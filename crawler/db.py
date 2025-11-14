import psycopg2
from psycopg2.extras import execute_values
from crawler.models import Repo

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            dbname="github_data",
            user="postgres",
            password="postgres"
        )
        self.conn.autocommit = True

    def create_schema(self):
        with self.conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS repositories (
                repo_id TEXT PRIMARY KEY,
                name TEXT,
                stars INTEGER,
                updated_at TIMESTAMP,
                last_crawled TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

    def upsert_repositories(self, repos: list[Repo]):
        with self.conn.cursor() as cur:
            values = [(r.repo_id, r.name, r.stars, r.updated_at) for r in repos]
            execute_values(cur, """
                INSERT INTO repositories (repo_id, name, stars, updated_at)
                VALUES %s
                ON CONFLICT (repo_id) DO UPDATE
                SET stars = EXCLUDED.stars,
                    updated_at = EXCLUDED.updated_at,
                    last_crawled = CURRENT_TIMESTAMP;
            """, values)