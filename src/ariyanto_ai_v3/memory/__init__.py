from loguru import logger
from .redis_memory import RedisMemory
from .sqlite_memory import SQLiteMemory

__all__ = ["MemoryManager", "get_memory_manager"]


class MemoryManager:
    HOT_AGENTS = {"MoonshotSolanaAgent", "FuturesSpecialist", "ICTSMCAgent", "RiskManager"}

    def __init__(self, redis_host="localhost", redis_port=6379, sqlite_path="./data/ariyanto_ai.db"):
        self.redis = RedisMemory(host=redis_host, port=redis_port)
        self.sqlite = SQLiteMemory(db_path=sqlite_path)
        logger.info("MemoryManager ready")

    def update_agent_state(self, agent_name: str, data: dict) -> bool:
        self.redis.set_agent_state(agent_name, data)
        return self.sqlite.set_agent_state(agent_name, data)

    def get_agent_state(self, agent_name: str):
        if agent_name in self.HOT_AGENTS:
            state = self.redis.get_agent_state(agent_name)
            if state: return state
        return self.sqlite.get_agent_state(agent_name)

    def log_audit(self, agent_name: str, action: str, details: dict):
        return self.sqlite.set_agent_state(agent_name, {"audit": details})


def get_memory_manager(**kwargs):
    return MemoryManager(**kwargs)