import logging
from typing import Sequence, Union
from enum import Enum
import mcp.types as types
from mcp.server import Server
from deepsearch.utils.search_utils import async_fetch_all_documents, async_process_documents_with_openrouter
from deepsearch.utils.pinecone_utils import PineconeManager
from deepsearch.utils.upload_to_cloudflare import CloudflareUploader
from deepsearch.utils.async_utils import log_cancellation

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("deepsearch-mcp")


class ToolName(str, Enum):
    PERFORM_ANALYSIS = "perform-analysis"


ServerTools = [
    types.Tool(
        name=ToolName.PERFORM_ANALYSIS,
        description="Passes the user query and uses it to search across the database documents.",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Natural language query to search across database documents"
                }
            },
            "required": ["query"],
        },
    ),
]


@log_cancellation
async def perform_search_analysis(
    query: str,
    pinecone_client: PineconeManager,
    cloudflare_uploader: CloudflareUploader,
    request_id: str,
    inflight_requests: dict
) -> Sequence[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Perform search analysis using Pinecone and Cloudflare
    """
    try:
        inflight_requests[request_id] = "running"

        if not query:
            logger.error("Empty query provided")
            raise ValueError("Query parameter is required")

        logger.info("Starting document retrieval and analysis...")

        # Step 1: Get search results and fetch documents
        search_results = pinecone_client.search_documents(
            query, min_normalized_score=0.5)
        logger.info(f"Retrieved {len(search_results)} documents")

        if inflight_requests.get(request_id) == "cancelled":
            return []

        # Step 2: Fetch documents
        documents = await async_fetch_all_documents(search_results, cloudflare_uploader)

        if inflight_requests.get(request_id) == "cancelled":
            return []

        # Step 3: Process documents with OpenRouter
        processed_results = await async_process_documents_with_openrouter(query, documents)

        if inflight_requests.get(request_id) == "cancelled":
            return []

        # Utility to strip out repeated "No relevant information..." lines
        def _clean_extracted_info(info: str) -> str:
            """
            Remove repeated "No relevant information found in the document." statements
            and return what's left. If nothing is left, it means there's no real info.
            """
            cleaned = info.replace(
                "No relevant information found in the document.", "")
            return cleaned.strip()

        # Filter out documents that end up with no actual content
        filtered_processed_results = {}
        for doc_path, raw_info in processed_results.items():
            cleaned_info = _clean_extracted_info(raw_info)
            # If there's still something left besides whitespace, we keep it; otherwise we skip
            if cleaned_info:
                filtered_processed_results[doc_path] = cleaned_info

        # If no documents had relevant information, return empty list
        if not filtered_processed_results:
            logger.info("No documents contained relevant information")
            inflight_requests[request_id] = "done"
            return [types.TextContent(type="text", text="No results found for the given query.")]

        # Combine results from filtered documents
        all_results = []
        for doc_path, info in filtered_processed_results.items():
            # Get the matching normalized score from search_results
            score = next(
                entry['normalized_score']
                for entry in search_results
                if entry['cloudflare_path'] == doc_path
            )
            all_results.append({
                'source': doc_path,
                'score': score,
                'extracted_info': info
            })

        # Sort by score in descending order
        results = sorted(all_results, key=lambda x: x['score'], reverse=True)

        # Format output for MCP
        formatted_output = []
        for result in results:
            section = [
                f"\nSource: {result['source']}",
                f"Score: {result['score']:.3f}",
                "Extracted Information:",
                f"{result['extracted_info']}",
                "=" * 80
            ]
            formatted_output.append("\n".join(section))

        inflight_requests[request_id] = "done"
        return [types.TextContent(type="text", text="\n".join(formatted_output))]

    except Exception as e:
        logger.error(f"Error in perform_search_analysis: {str(e)}")
        inflight_requests[request_id] = "error"
        raise


def register_tools(server: Server, pinecone_client: PineconeManager, cloudflare_uploader: CloudflareUploader, inflight_requests: dict):
    @server.list_tools()
    @log_cancellation
    async def handle_list_tools() -> list[types.Tool]:
        return ServerTools

    @server.call_tool()
    @log_cancellation
    async def handle_call_tool(
        name: str, arguments: dict | None
    ) -> Sequence[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
        try:
            # You'll need to ensure this is passed
            request_id = arguments.get("__request_id__")
            logger.info(f"Calling tool: {name} for request {request_id}")

            if name == ToolName.PERFORM_ANALYSIS:
                return await perform_search_analysis(
                    query=arguments.get("query"),
                    pinecone_client=pinecone_client,
                    cloudflare_uploader=cloudflare_uploader,
                    request_id=request_id,
                    inflight_requests=inflight_requests
                )
            else:
                logger.error(f"Unknown tool: {name}")
                raise ValueError(f"Unknown tool: {name}")
        except Exception as e:
            logger.error(f"Error calling tool {name}: {str(e)}")
            raise


__all__ = [
    "register_tools",
]
