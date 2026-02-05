import sqlite3
from pathlib import Path

# This creates/uses a database file at: backend/mealpro.db
BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
DB_PATH = BASE_DIR / "mealpro.db"


def get_connection() -> sqlite3.Connection:
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # allows dict-like access
    return conn


def init_db() -> None:
    """Create tables if they don't exist."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                diet_tags TEXT,
                prep_minutes INTEGER,
                cook_minutes INTEGER,
                ingredients TEXT,
                instructions TEXT
            );
            """
        )
        conn.commit()
