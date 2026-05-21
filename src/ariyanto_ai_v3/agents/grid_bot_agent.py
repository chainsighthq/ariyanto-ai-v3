from __future__ import annotations
import re
from typing import Any, Dict
from ariyanto_ai_v3.core.models import AgentResult, Task
from ariyanto_ai_v3.agents.base_agent import BaseAgent

class GridBotAgent(BaseAgent):
    name = "GridBotAgent"
    description = "Grid trading bot setup"
    def think(self, task: Task) -> Dict[str, Any]:
        symbol_match = re.search(r"\b(btc|eth|sol)\b", task.user_input.lower())
        symbol = symbol_match.group(1).upper() if symbol_match else "BTC"
        return {"symbol": symbol}
    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        return AgentResult(task_id=task.task_id, agent_name=self.name, success=True, message=f"Grid Bot ({reasoning['symbol']}): Range $75K-$85K, 20 grids, 1% spacing. Est. APY: 45-65% in sideways market.", result_data={"symbol": reasoning['symbol'], "range": "75K-85K", "grids": 20, "est_apy": "45-65%"}, simulation=self.simulation)
