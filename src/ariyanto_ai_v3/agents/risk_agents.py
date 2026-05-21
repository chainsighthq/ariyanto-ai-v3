from __future__ import annotations
from typing import Any, Dict
from ariyanto_ai_v3.core.models import AgentResult, RiskMetrics, Task
from ariyanto_ai_v3.agents.base_agent import BaseAgent


class RiskManager(BaseAgent):
    name = "RiskManager"
    description = "Portfolio risk & drawdown protection"

    def __init__(self, memory_manager=None, simulation=True, max_drawdown=3.0):
        super().__init__(memory_manager, simulation)
        self.max_drawdown = max_drawdown

    def think(self, task: Task) -> Dict[str, Any]:
        return {"type": "risk_check"}

    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        portfolio_value = 10000.0
        peak = 10500.0
        current_drawdown = round((peak - portfolio_value) / peak * 100, 2)

        metrics = RiskMetrics(
            portfolio_value=portfolio_value,
            drawdown_percent=current_drawdown,
            max_drawdown_allowed=self.max_drawdown
        )

        self.memory.update_agent_state(self.name, metrics.model_dump())

        if current_drawdown > self.max_drawdown:
            message = f"DRAWDOWN BREACH! {current_drawdown}% > {self.max_drawdown}%"
            alerts = ["CRITICAL: Drawdown breach detected"]
        else:
            message = f"Risk OK. Current drawdown: {current_drawdown}%"
            alerts = []

        return AgentResult(
            task_id=task.task_id,
            agent_name=self.name,
            success=True,
            message=message,
            result_data={"risk_metrics": metrics.model_dump()},
            alerts=alerts,
            simulation=self.simulation,
        )
