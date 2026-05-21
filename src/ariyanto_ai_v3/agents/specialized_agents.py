from __future__ import annotations
from typing import Any, Dict
from ariyanto_ai_v3.core.models import AgentResult, Task
from ariyanto_ai_v3.agents.base_agent import BaseAgent


class GeneralAnalysisAgent(BaseAgent):
    name = "GeneralAnalysisAgent"
    description = "Fallback general analysis agent"

    def think(self, task: Task) -> Dict[str, Any]:
        return {"type": "general", "query": task.user_input}

    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        return AgentResult(
            task_id=task.task_id,
            agent_name=self.name,
            success=True,
            message=f"General analysis for: '{task.user_input}'. Try using more specific keywords like 'Long BTC', 'ICT XAGUSD', or 'check risk'.",
            result_data={"suggestion": "Use keywords like: Long, ICT, analyze, risk, arbitrage"},
            simulation=self.simulation,
        )
