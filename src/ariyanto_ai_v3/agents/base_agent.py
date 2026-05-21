from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from loguru import logger
import time
from uuid import uuid4

from ..core.models import AgentResult, Task, RiskMetrics
from ..memory import MemoryManager
from ..config import settings

class BaseAgent(ABC):
    name: str = "BaseAgent"
    tier: int = 2
    description: str = ""
    
    def __init__(self, memory_manager: Optional[MemoryManager] = None, simulation: bool = True):
        self.memory = memory_manager or MemoryManager()
        self.simulation = simulation or (settings.EXECUTION_MODE == "simulation")
        self.correlation_id = str(uuid4())
    
    def run(self, task: Task) -> AgentResult:
        start_time = time.time()
        logger.info(f"[{self.name}] Received task | correlation={self.correlation_id[:8]}")
        
        try:
            reasoning = self.think(task)
            result = self.act(reasoning, task)
            result.execution_time_ms = (time.time() - start_time) * 1000
            result.correlation_id = self.correlation_id
            result.simulation = self.simulation
            
            logger.info(f"[{self.name}] Completed in {result.execution_time_ms:.1f}ms | success={result.success}")
            return result
            
        except Exception as e:
            logger.error(f"[{self.name}] Error: {e}")
            return AgentResult(
                task_id=task.task_id,
                agent_name=self.name,
                success=False,
                error=str(e),
                execution_time_ms=(time.time() - start_time) * 1000,
                simulation=self.simulation,
                correlation_id=self.correlation_id
            )
    
    @abstractmethod
    def think(self, task: Task) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        pass
    
    def log_action(self, action: str, details: Dict[str, Any]):
        """Log action to memory for audit trail"""
        self.memory.log_audit(
            agent_name=self.name,
            action=action,
            details=details,
            correlation_id=self.correlation_id,
            simulation=self.simulation
        )
