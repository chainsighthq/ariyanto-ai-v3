import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from loguru import logger


class SQLiteMemory:
    def __init__(self, db_path: str = "./data/ariyanto_ai.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS agent_states (
                    agent_name TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    last_updated TEXT NOT NULL
                )
            """)
            conn.commit()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(str(self.db_path), timeout=10)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def set_agent_state(self, agent_name: str, data: Dict[str, Any]) -> bool:
        try:
            with self._get_connection() as conn:
                now = datetime.now(timezone.utc).isoformat()
                conn.execute("INSERT OR REPLACE INTO agent_states (agent_name, data, last_updated) VALUES (?, ?, ?)", (agent_name, json.dumps(data, default=str), now))
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"SQLite error: {e}")
            return False

    def get_agent_state(self, agent_name: str) -> Optional[Dict[str, Any]]:
        try:
            with self._get_connection() as conn:
                row = conn.execute("SELECT data, last_updated FROM agent_states WHERE agent_name = ?", (agent_name,)).fetchone()
                if row:
                    return {"data": json.loads(row["data"]), "last_updated": row["last_updated"]}
                return None
        except Exception:
            return None