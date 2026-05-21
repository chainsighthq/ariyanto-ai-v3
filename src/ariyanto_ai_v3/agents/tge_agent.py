from __future__ import annotations
import re
from typing import Any, Dict
from ariyanto_ai_v3.core.models import AgentResult, Task
from ariyanto_ai_v3.agents.base_agent import BaseAgent

class TGEAgent(BaseAgent):
    name = "TGEAgent"
    description = "TGE/Launch detection & analysis"
    def think(self, task: Task) -> Dict[str, Any]:
        project_match = re.search(r"\b(berachain|layerzero|celestia|eigenlayer)\b", task.user_input.lower())
        project = project_match.group(1).title() if project_match else "Berachain"
        return {"project": project}
    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        project = reasoning["project"]
        return AgentResult(task_id=task.task_id, agent_name=self.name, success=True, message=f"TGE Alert: {project} TGE expected in 2-4 weeks. FDV estimate: $800M-$1.2B. Recommended allocation: 0.5-1% portfolio.", result_data={"project": project, "expected_tge": "2-4 weeks", "fdv_estimate": "$800M-$1.2B"}, simulation=self.simulation)
