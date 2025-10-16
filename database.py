import sqlite3
from pydantic import BaseModel, Field
import pandas as pd

class RepoInfo(BaseModel):
    repo_name: str = Field(description="The name of the repository (e.g., 'user/repo').")
    url: str = Field(description="The full URL to the GitHub repository.")
    description: str = Field(description="A one-sentence summary of the repository's purpose.")
    stars: int = Field(description="The number of stars the repository has.")
    primary_language: str = Field(description="The primary programming language of the repository.")
    why_it_matches: str = Field(description="A brief analysis explaining why this repository is a good match based on the user's query.")

def init_db(db_name: str = "repositories.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS repositories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        repo_name TEXT NOT NULL UNIQUE,
        url TEXT,
        description TEXT,
        stars INTEGER,
        primary_language TEXT,
        why_it_matches TEXT
    )
    """)
    conn.commit()
    conn.close()
    print("Repository database initialized successfully.")

def add_repo(repo: RepoInfo, db_name: str = "repositories.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO repositories (repo_name, url, description, stars, primary_language, why_it_matches)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                repo.repo_name, repo.url, repo.description, repo.stars,
                repo.primary_language, repo.why_it_matches
            )
        )
        conn.commit()
        print(f"Successfully added repository: {repo.repo_name}")
    except sqlite3.IntegrityError:
        print(f"Repository already exists for: {repo.repo_name}. Skipping.")
    finally:
        conn.close()

def get_all_repos(db_name: str = "repositories.db") -> pd.DataFrame:
    conn = sqlite3.connect(db_name)
    try:
        df = pd.read_sql_query("SELECT * FROM repositories ORDER BY stars DESC", conn)
        return df
    except Exception as e:
        print(f"An error occurred while fetching repositories: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

