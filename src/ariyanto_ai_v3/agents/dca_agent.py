from __future__ import annotations
import re
from typing import Any, Dict
from ariyanto_ai_v3.core.models import AgentResult, Task
from ariyanto_ai_v3.agents.base_agent import BaseAgent
class DCAAgent(BaseAgent):
    name = "DCAAgent"
    def think(self, task: Task) -> Dict[str, Any]:
        symbol_match = re.search(r"\b(btc|eth|sol)\b", task.user_input.lower())
        symbol = symbol_match.group(1).upper() if symbol_match else "BTC"
        return {"symbol": symbol}
    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        return AgentResult(task_id=task.task_id, agent_name=self.name, success=True, message=f"DCA Strategy ({reasoning['symbol']}): Buy $500/week. Current avg: $68,400. Next buy in 3 days. Total invested: $12,400. Current value: $14,200 (+14.5%).", simulation=self.simulation)
