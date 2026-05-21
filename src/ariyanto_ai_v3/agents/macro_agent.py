from __future__ import annotations
from typing import Any, Dict
from ariyanto_ai_v3.core.models import AgentResult, Task
from ariyanto_ai_v3.agents.base_agent import BaseAgent

class MacroAgent(BaseAgent):
    name = "MacroAgent"
    description = "Macro & sentiment analysis"
    def think(self, task: Task) -> Dict[str, Any]:
        return {"type": "macro"}
    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        return AgentResult(task_id=task.task_id, agent_name=self.name, success=True, message="Macro Analysis: Fed policy dovish, DXY -0.8%, Risk-on sentiment dominant. BTC correlation with Nasdaq at 0.72.", result_data={"dxy": -0.8, "sentiment": "Risk-on", "btc_nasdaq_corr": 0.72}, simulation=self.simulation)
