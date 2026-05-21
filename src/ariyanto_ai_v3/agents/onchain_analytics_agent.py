from __future__ import annotations
import re
from typing import Any, Dict
from ariyanto_ai_v3.core.models import AgentResult, Task
from ariyanto_ai_v3.agents.base_agent import BaseAgent

class OnChainAnalyticsAgent(BaseAgent):
    name = "OnChainAnalyticsAgent"
    description = "On-chain metrics & analytics"
    def think(self, task: Task) -> Dict[str, Any]:
        symbol_match = re.search(r"\b(btc|eth|sol)\b", task.user_input.lower())
        symbol = symbol_match.group(1).upper() if symbol_match else "BTC"
        return {"symbol": symbol}
    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        return AgentResult(task_id=task.task_id, agent_name=self.name, success=True, message=f"On-Chain ({reasoning['symbol']}): Active addresses +12%, Exchange inflow -8% (bullish), MVRV: 2.1 (fair value), SOPR: 1.05 (profit taking).", result_data={"symbol": reasoning['symbol'], "active_addresses": "+12%", "exchange_inflow": "-8%", "mvrv": 2.1}, simulation=self.simulation)
