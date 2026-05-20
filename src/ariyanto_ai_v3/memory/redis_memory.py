import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import redis
from loguru import logger


class RedisMemory:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, password: Optional[str] = None):
        self.client = redis.Redis(host=host, port=port, db=db, password=password, decode_responses=True)
        try:
            self.client.ping()
            logger.info("Redis connected")
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")

    def set_agent_state(self, agent_name: str, data: Dict[str, Any]) -> bool:
        key = f"agent:{agent_name}"
        try:
            self.client.hset(key, mapping={"last_updated": datetime.now(timezone.utc).isoformat(), "data": json.dumps(data, default=str)})
            return True
        except Exception as e:
            logger.error(f"Redis error: {e}")
            return False

    def get_agent_state(self, agent_name: str) -> Optional[Dict[str, Any]]:
        key = f"agent:{agent_name}"
        try:
            raw = self.client.hgetall(key)
            if raw:
                return {"last_updated": raw.get("last_updated"), "data": json.loads(raw.get("data", "{}"))}
            return None
        except Exception:
            return None