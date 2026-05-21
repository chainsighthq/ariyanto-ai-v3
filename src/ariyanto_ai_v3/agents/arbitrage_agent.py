from __future__ import annotations
import re
from typing import Any, Dict
from ariyanto_ai_v3.core.models import AgentResult, Task
from ariyanto_ai_v3.agents.base_agent import BaseAgent

class ArbitrageAgent(BaseAgent):
    name = "ArbitrageAgent"
    description = "Cross-exchange & CEX-DEX arbitrage"
    def think(self, task: Task) -> Dict[str, Any]:
        symbol_match = re.search(r"\b(btc|eth|sol)\b", task.user_input.lower())
        symbol = symbol_match.group(1).upper() if symbol_match else "BTC"
        return {"symbol": symbol}
    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        symbol = reasoning["symbol"]
        return AgentResult(task_id=task.task_id, agent_name=self.name, success=True, message=f"Arbitrage Scan ({symbol}): Binance-Kraken spread 0.12%, Binance-Uniswap spread 0.28%. Best opportunity: Binance → Uniswap (0.28% after fees).", result_data={"symbol": symbol, "cex_spread": 0.12, "dex_spread": 0.28, "best_route": "Binance → Uniswap"}, simulation=self.simulation)
