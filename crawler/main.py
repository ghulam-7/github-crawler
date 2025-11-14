import asyncio, time
from crawler.github_client import GitHubClient
from crawler.db import Database

async def main():
    start = time.time()
    print("🚀 Starting GitHub crawl...")

    client = GitHubClient()
    db = Database()
    db.create_schema()

    repos = await client.fetch_repositories(target_count=100000)
    db.upsert_repositories(repos)

    end = time.time()
    print(f"✅ Completed 100,000 repos in {(end - start)/60:.2f} minutes")

if __name__ == "__main__":
    asyncio.run(main())