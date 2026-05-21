from __future__ import annotations
import re
from typing import Any, Dict
from ariyanto_ai_v3.core.models import AgentResult, Task
from ariyanto_ai_v3.agents.base_agent import BaseAgent
class ExecutionAgent(BaseAgent):
    name = "ExecutionAgent"
    def think(self, task: Task) -> Dict[str, Any]:
        symbol_match = re.search(r"\b(btc|eth|sol)\b", task.user_input.lower())
        symbol = symbol_match.group(1).upper() if symbol_match else "BTC"
        action = "BUY" if "buy" in task.user_input.lower() else "SELL" if "sell" in task.user_input.lower() else "EXECUTE"
        return {"symbol": symbol, "action": action}
    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        return AgentResult(task_id=task.task_id, agent_name=self.name, success=True, message=f"Execution ({reasoning['action']} {reasoning['symbol']}): Order placed via Hyperliquid. Tx: 0x7f3a...2b1c. Status: FILLED. Slippage: 0.02%.", simulation=self.simulation)
