from .redis_memory import RedisMemory
from .sqlite_memory import SQLiteMemory
from typing import Optional, Dict, Any
from loguru import logger
import json
from datetime import datetime, date

def _make_json_safe(obj: Any) -> Any:
    """Recursively convert datetime objects to ISO strings"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: _make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_make_json_safe(item) for item in obj]
    return obj

class MemoryManager:
    def __init__(self):
        self.redis = RedisMemory()
        self.sqlite = SQLiteMemory()
        logger.info("Hybrid MemoryManager initialized (Redis + SQLite WAL)")
    
    def set_agent_state(self, agent_name: str, data: Dict[str, Any], use_redis: bool = True):
        safe_data = _make_json_safe(data)
        
        if use_redis:
            try:
                self.redis.set_agent_state(agent_name, safe_data)
            except Exception as e:
                logger.debug(f"Redis set failed (non-critical): {e}")
        
        self.sqlite.set_agent_state(agent_name, safe_data)
    
    def get_agent_state(self, agent_name: str) -> Optional[Dict[str, Any]]:
        state = self.redis.get_agent_state(agent_name)
        if state is None:
            state = self.sqlite.get_agent_state(agent_name)
        return state
    
    def log_audit(self, agent_name: str, action: str, details: Dict[str, Any], 
                  correlation_id: str = "", simulation: bool = True):
        safe_details = _make_json_safe(details)
        self.sqlite.log_audit(agent_name, action, safe_details, correlation_id, simulation)
    
    def update_agent_state(self, agent_name: str, data: Dict[str, Any]):
        """Alias for set_agent_state (backward compatibility)"""
        self.set_agent_state(agent_name, data)
