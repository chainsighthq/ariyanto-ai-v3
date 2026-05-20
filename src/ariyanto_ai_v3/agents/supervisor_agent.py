from __future__ import annotations

from typing import Any, Dict, Optional, Type

from loguru import logger

from ..core.models import AgentResult, Task

from ..core.router import router

from ..memory import MemoryManager

from .base_agent import BaseAgent

# Import specialists
try:
    from .trading_agents import FuturesSpecialist, MoonshotSolanaAgent
    from .intelligence_agents import IntelligenceResearchAgent, TradingViewMCPAgent
    from .onchain_agents import ICTSMCAgent, OnChainAnalyst
    from .risk_agents import RiskManager
    from .wallet_agents import WalletManager
    from .specialized_agents import GeneralAnalysisAgent
except ImportError:
    pass


class SupervisorAgent(BaseAgent):
    name = "SupervisorAgent"
    tier = 1
    description = "Main orchestrator"

    def __init__(self, memory_manager: Optional[MemoryManager] = None, simulation: bool = True):
        super().__init__(memory_manager, simulation)
        self._agent_registry = self._build_registry()

    def _build_registry(self):
        return {
            "FuturesSpecialist": FuturesSpecialist,
            "MoonshotSolanaAgent": MoonshotSolanaAgent,
            "IntelligenceResearchAgent": IntelligenceResearchAgent,
            "TradingViewMCPAgent": TradingViewMCPAgent,
            "ICTSMCAgent": ICTSMCAgent,
            "OnChainAnalyst": OnChainAnalyst,
            "RiskManager": RiskManager,
            "WalletManager": WalletManager,
            "GeneralAnalysisAgent": GeneralAnalysisAgent,
        }

    def think(self, task: Task) -> Dict[str, Any]:
        agent_name = router.get_agent_class_name(task.user_input)
        return {
            "routed_to": agent_name,
            "original_input": task.user_input,
        }

    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        agent_name = reasoning.get("routed_to", "GeneralAnalysisAgent")
        AgentClass = self._agent_registry.get(agent_name, GeneralAnalysisAgent)
        try:
            specialist = AgentClass(memory_manager=self.memory, simulation=self.simulation)
            specialist_result = specialist.run(task)
            return AgentResult(
                task_id=task.task_id,
                agent_name=self.name,
                success=specialist_result.success,
                result_data={"routed_to": agent_name, "specialist_result": specialist_result.model_dump()},
                message=f"Delegated to {agent_name}. {specialist_result.message}",
                alerts=specialist_result.alerts,
                simulation=self.simulation,
            )
        except Exception as e:
            return AgentResult(
                task_id=task.task_id,
                agent_name=self.name,
                success=False,
                message=f"Delegation failed: {str(e)}",
                error=str(e),
                simulation=self.simulation,
            )