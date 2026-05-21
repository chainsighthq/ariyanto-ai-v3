from ..core.models import AgentResult, Task
from .base_agent import BaseAgent
from typing import Dict, Any

class GeneralAnalysisAgent(BaseAgent):
    name = "GeneralAnalysisAgent"
    description = "Fallback general analysis"
    
    def think(self, task: Task) -> Dict[str, Any]:
        return {"action": "GENERAL_ANALYSIS", "query": task.user_input}
    
    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        return AgentResult(
            task_id=task.task_id,
            agent_name=self.name,
            success=True,
            message=f"General analysis for: '{reasoning['query']}'. Try using more specific keywords like 'Long BTC', 'ICT XAGUSD', or 'check risk'.",
            simulation=self.simulation
        )
