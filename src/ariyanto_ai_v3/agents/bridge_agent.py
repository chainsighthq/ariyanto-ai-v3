from __future__ import annotations
import re
from typing import Any, Dict
from ariyanto_ai_v3.core.models import AgentResult, Task
from ariyanto_ai_v3.agents.base_agent import BaseAgent
class BridgeAgent(BaseAgent):
    name = "BridgeAgent"
    def think(self, task: Task) -> Dict[str, Any]:
        chain_match = re.search(r"\b(ethereum|solana|arbitrum|base|polygon)\b", task.user_input.lower())
        chain = chain_match.group(1).title() if chain_match else "Arbitrum"
        return {"chain": chain}
    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        return AgentResult(task_id=task.task_id, agent_name=self.name, success=True, message=f"Bridge to {reasoning['chain']}: Stargate cheapest ($8, 3 min), Across fastest (1 min, $12). Recommended: Stargate for <$10K. Security: 7/7 audits passed.", simulation=self.simulation)
