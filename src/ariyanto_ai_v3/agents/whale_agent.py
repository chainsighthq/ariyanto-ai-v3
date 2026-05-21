from __future__ import annotations
import re
from typing import Any, Dict
from ariyanto_ai_v3.core.models import AgentResult, Task
from ariyanto_ai_v3.agents.base_agent import BaseAgent

class WhaleAgent(BaseAgent):
    name = "WhaleAgent"
    description = "On-chain whale movement detector"
    def think(self, task: Task) -> Dict[str, Any]:
        symbol_match = re.search(r"\b(btc|eth|sol|usdt)\b", task.user_input.lower())
        symbol = symbol_match.group(1).upper() if symbol_match else "BTC"
        return {"symbol": symbol}
    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        symbol = reasoning["symbol"]
        return AgentResult(task_id=task.task_id, agent_name=self.name, success=True, message=f"Whale Alert: Large {symbol} transfer detected (2,450 {symbol} \~ $195M). Exchange inflow +12% in last hour.", result_data={"symbol": symbol, "whale_volume": 2450, "usd_value": 195000000, "exchange_inflow_pct": 12}, simulation=self.simulation)
