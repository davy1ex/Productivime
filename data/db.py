import os
import sqlite3
from typing import List, Tuple, Optional

DB_PATH = os.path.join("data", "scores.db")

class DBManager:
    """Tiny SQLite helper for scores table."""
    def __init__(self, db_path: str = DB_PATH):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._ensure_schema()

    def _connect(self):
        # isolation_level=None for autocommit OFF; we commit manually
        return sqlite3.connect(self.db_path)

    def _ensure_schema(self):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    delivered INTEGER NOT NULL,
                    time_spent INTEGER NOT NULL,
                    reason TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Helpful index for ordering by score
            cur.execute("CREATE INDEX IF NOT EXISTS idx_scores_score ON scores(score DESC)")
            conn.commit()

    def insert_score(self, name: str, score: int, delivered: int, time_spent: int, reason: str) -> int:
        """Insert one row, return inserted id."""
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO scores(name, score, delivered, time_spent, reason) VALUES(?,?,?,?,?)",
                (name, int(score), int(delivered), int(time_spent), reason)
            )
            conn.commit()
            return cur.lastrowid

    def top5(self) -> List[Tuple[str,int,int,int,str,str]]:
        """Return top 5 by score desc, tuple fields: (name, score, delivered, time_spent, reason, created_at)."""
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT name, score, delivered, time_spent, reason, created_at
                FROM scores
                ORDER BY score DESC, time_spent ASC
                LIMIT 5
            """)
            return cur.fetchall()
