from __future__ import annotations

import time
import traceback
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from uuid import uuid4

from loguru import logger

from ..core.models import AgentResult, Task
from ..memory import MemoryManager


class BaseAgent(ABC):
    """
    Abstract base for all agents in the hierarchy.
    Every agent follows:
        1. think() -> parse & reason
        2. act() -> execute safely
    """

    name: str = "BaseAgent"
    tier: int = 2
    description: str = "Base agent"

    def __init__(self, memory_manager: Optional[MemoryManager] = None, simulation: bool = True):
        self.memory = memory_manager or MemoryManager()
        self.simulation = simulation
        self.correlation_id: Optional[str] = None
        self._last_result: Optional[AgentResult] = None

    @abstractmethod
    def think(self, task: Task) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        raise NotImplementedError

    def run(self, task: Task) -> AgentResult:
        start = time.perf_counter()
        self.correlation_id = task.correlation_id or str(uuid4())[:8]
        logger.info(f"[{self.name}] Received task | correlation={self.correlation_id}")

        try:
            reasoning = self.think(task)
            result = self.act(reasoning, task)
            self.memory.update_agent_state(self.name, {
                "last_task_id": task.task_id,
                "last_input": task.user_input,
                "last_success": result.success,
            })
            self.memory.log_audit(self.name, "task_executed", {"task_id": task.task_id, "success": result.success})
            elapsed = (time.perf_counter() - start) * 1000
            result.execution_time_ms = round(elapsed, 2)
            result.simulation = self.simulation
            self._last_result = result
            logger.info(f"[{self.name}] Completed in {elapsed:.1f}ms")
            return result
        except Exception as exc:
            logger.exception(f"[{self.name}] CRITICAL FAILURE")
            elapsed = (time.perf_counter() - start) * 1000
            return AgentResult(
                task_id=task.task_id,
                agent_name=self.name,
                success=False,
                message=f"Agent failed: {str(exc)[:200]}",
                error=str(exc),
                execution_time_ms=round(elapsed, 2),
                simulation=self.simulation,
            )