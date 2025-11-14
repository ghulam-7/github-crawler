import os, aiohttp, asyncio, time
from typing import List, Tuple
from crawler.models import Repo

class GitHubClient:
    def __init__(self):
        self.endpoint = "https://api.github.com/graphql"
        self.headers = {"Authorization": f"bearer {os.environ.get('GITHUB_TOKEN')}"}
        self.query = """
        query ($cursor: String) {
          search(query: "stars:>1", type: REPOSITORY, first: 100, after: $cursor) {
            edges {
              node {
                ... on Repository {
                  id
                  nameWithOwner
                  stargazerCount
                  updatedAt
                }
              }
            }
            pageInfo {
              endCursor
              hasNextPage
            }
          }
        }
        """

    async def fetch_page(self, session, cursor=None) -> Tuple[List[Repo], str]:
        payload = {"query": self.query, "variables": {"cursor": cursor}}
        async with session.post(self.endpoint, json=payload, headers=self.headers) as resp:
            if resp.status == 403:
                print("⏳ Rate limit hit, waiting 60s...")
                await asyncio.sleep(60)
                return await self.fetch_page(session, cursor)
            data = await resp.json()
            search = data["data"]["search"]
            repos = [
                Repo(
                    repo_id=edge["node"]["id"],
                    name=edge["node"]["nameWithOwner"],
                    stars=edge["node"]["stargazerCount"],
                    updated_at=edge["node"]["updatedAt"],
                )
                for edge in search["edges"]
            ]
            next_cursor = search["pageInfo"]["endCursor"] if search["pageInfo"]["hasNextPage"] else None
            return repos, next_cursor

    async def fetch_repositories(self, target_count=100000) -> List[Repo]:
        all_repos, cursor = [], None
        async with aiohttp.ClientSession() as session:
            while len(all_repos) < target_count:
                repos, cursor = await self.fetch_page(session, cursor)
                all_repos.extend(repos)
                print(f"Fetched {len(all_repos)} repositories...")
                if not cursor:
                    break
                await asyncio.sleep(1)
        return all_repos[:target_count]