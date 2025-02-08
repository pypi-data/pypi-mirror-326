import asyncio
from deepsearch.utils.search_utils import perform_search_analysis
from deepsearch.utils.pinecone_utils import PineconeManager
from deepsearch.utils.upload_to_cloudflare import CloudflareUploader


async def main(
    query: str,
    output_dir: str = "test_output",
    outlier_method: str = 'zscore',
    outlier_threshold: float = 1
):
    # Initialize clients
    pinecone_client = PineconeManager()
    cloudflare_uploader = CloudflareUploader()

    results = await perform_search_analysis(
        query=query,
        pinecone_client=pinecone_client,
        cloudflare_uploader=cloudflare_uploader
    )

    # Print results
    for result in results:
        print(f"\nSource: {result['source']}")
        print(f"Score: {result['score']:.3f}")
        print("Extracted Information:")
        print(result['extracted_info'])
        print("="*80)


if __name__ == "__main__":
    query = "What was the carbon feed rate at the beginning, and at the end of the run? On a grams of sucrose / L hr basis at the October sucrose run at Laurus Bio."
    print(f"Starting search with query: {query}")
    asyncio.run(main(query))
    print("Script finished!")
