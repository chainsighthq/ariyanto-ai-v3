import sqlite3
import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from loguru import logger

class SQLiteMemory:
    def __init__(self, db_path: str = "./data/ariyanto_ai.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Drop old table if exists (for dev only - in production use migration)
        # cursor.execute("DROP TABLE IF EXISTS agent_states")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_states (
                agent_name TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT,
                action TEXT,
                details TEXT,
                correlation_id TEXT,
                simulation INTEGER DEFAULT 1,
                timestamp TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        logger.debug("SQLite schema initialized")
    
    def set_agent_state(self, agent_name: str, data: Dict[str, Any]):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO agent_states (agent_name, data, timestamp)
            VALUES (?, ?, ?)
        """, (
            agent_name, 
            json.dumps(data, default=str), 
            datetime.now(timezone.utc).isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def get_agent_state(self, agent_name: str) -> Optional[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT data FROM agent_states WHERE agent_name = ?", (agent_name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return json.loads(row[0])
        return None
    
    def log_audit(self, agent_name: str, action: str, details: Dict[str, Any], 
                  correlation_id: str = "", simulation: bool = True):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO audit_log (agent_name, action, details, correlation_id, simulation, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            agent_name,
            action,
            json.dumps(details, default=str),
            correlation_id,
            1 if simulation else 0,
            datetime.now(timezone.utc).isoformat()
        ))
        
        conn.commit()
        conn.close()
