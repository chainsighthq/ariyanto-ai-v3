from __future__ import annotations
import re
from typing import Any, Dict
from ariyanto_ai_v3.core.models import AgentResult, Task
from ariyanto_ai_v3.agents.base_agent import BaseAgent

class SentimentAgent(BaseAgent):
    name = "SentimentAgent"
    description = "Social sentiment & narrative tracker"
    def think(self, task: Task) -> Dict[str, Any]:
        symbol_match = re.search(r"\b(btc|eth|sol|xrp)\b", task.user_input.lower())
        symbol = symbol_match.group(1).upper() if symbol_match else "BTC"
        return {"symbol": symbol}
    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        symbol = reasoning["symbol"]
        return AgentResult(task_id=task.task_id, agent_name=self.name, success=True, message=f"Sentiment Analysis ({symbol}): Twitter 72% bullish, Telegram 68% bullish, Fear & Greed: 72 (Greed). Narrative: ETF approval momentum.", result_data={"symbol": symbol, "twitter_bullish": 72, "telegram_bullish": 68, "fear_greed": 72}, simulation=self.simulation)
