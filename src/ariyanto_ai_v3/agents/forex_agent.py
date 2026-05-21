from __future__ import annotations
import re
from typing import Any, Dict
from ariyanto_ai_v3.core.models import AgentResult, Task
from ariyanto_ai_v3.agents.base_agent import BaseAgent
class ForexSpecialist(BaseAgent):
    name = "ForexSpecialist"
    def think(self, task: Task) -> Dict[str, Any]:
        pair_match = re.search(r"\b(eurusd|gbpusd|usdjpy|xagusd|xauusd)\b", task.user_input.lower())
        pair = pair_match.group(1).upper() if pair_match else "XAGUSD"
        return {"pair": pair}
    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        return AgentResult(task_id=task.task_id, agent_name=self.name, success=True, message=f"Forex Analysis ({reasoning['pair']}): D1 bullish, H4 consolidation. Key levels: Support $31.20, Resistance $32.80. Bias: BULLISH. Entry: $31.45. SL: $30.80. TP: $32.50.", simulation=self.simulation)
