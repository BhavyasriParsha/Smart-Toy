"""
Database Service — SQLite conversation storage
Uses Python's built-in sqlite3 (no extra install needed).
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "smart_toy.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if they don't exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                query     TEXT    NOT NULL,
                intent    TEXT    NOT NULL DEFAULT 'unknown',
                response  TEXT    NOT NULL,
                timestamp TEXT    NOT NULL
            )
        """)
        conn.commit()


def save_conversation(query: str, intent: str, response: str) -> None:
    """Persist a single conversation turn."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO conversations (query, intent, response, timestamp) VALUES (?, ?, ?, ?)",
            (query, intent, response, datetime.utcnow().isoformat()),
        )
        conn.commit()


def get_history(limit: int = 50) -> list[dict]:
    """Return the most recent conversations, newest last."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT query, intent, response, timestamp FROM conversations ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in reversed(rows)]
