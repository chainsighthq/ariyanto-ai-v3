from __future__ import annotations
import re
from typing import Any, Dict
from ariyanto_ai_v3.core.models import AgentResult, Task
from ariyanto_ai_v3.agents.base_agent import BaseAgent


class ICTSMCAgent(BaseAgent):
    name = "ICTSMCAgent"
    description = "ICT / Smart Money Concepts analysis"

    def think(self, task: Task) -> Dict[str, Any]:
        symbol_match = re.search(r"\b(xagusd|btc|eth|sol)\b", task.user_input.lower())
        symbol = symbol_match.group(1).upper() if symbol_match else "XAGUSD"
        return {"symbol": symbol}

    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        return AgentResult(
            task_id=task.task_id,
            agent_name=self.name,
            success=True,
            message=f"ICT/SMC analysis for {reasoning['symbol']} completed. Bullish displacement phase detected (simulated).",
            result_data={"phase": "Bullish Displacement"},
            simulation=self.simulation,
        )
