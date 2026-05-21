from __future__ import annotations
import re
from typing import Any, Dict
from ariyanto_ai_v3.core.models import AgentResult, Task
from ariyanto_ai_v3.agents.base_agent import BaseAgent

class FundingRateAgent(BaseAgent):
    name = "FundingRateAgent"
    description = "Perpetual funding rate analysis"
    def think(self, task: Task) -> Dict[str, Any]:
        symbol_match = re.search(r"\b(btc|eth|sol)\b", task.user_input.lower())
        symbol = symbol_match.group(1).upper() if symbol_match else "BTC"
        return {"symbol": symbol}
    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        symbol = reasoning["symbol"]
        return AgentResult(task_id=task.task_id, agent_name=self.name, success=True, message=f"Funding Rate ({symbol}): Current +0.012% (bullish bias). 8h avg: +0.008%. Longs paying shorts. OI: $2.8B. Recommended: Hold long bias.", result_data={"symbol": symbol, "funding_8h": 0.012, "oi_usd": 2800000000, "bias": "bullish"}, simulation=self.simulation)
