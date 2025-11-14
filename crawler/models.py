from dataclasses import dataclass

@dataclass(frozen=True)
class Repo:
    repo_id: str
    name: str
    stars: int
    updated_at: str