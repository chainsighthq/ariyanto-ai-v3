import re
from typing import Dict

from loguru import logger


class KeywordRouter:
    def __init__(self):
        self._routes: Dict[str, str] = {
            r"\b(long|short|trade|futures?|leverage|10x|5x)\b.*\b(btc|eth|sol)\b": "FuturesSpecialist",
            r"\b(moonshot|arbitrage|jupiter)\b.*\b(sol|solana)\b": "MoonshotSolanaAgent",
            r"\b(analyze|fundamental|news|catalyst)\b": "IntelligenceResearchAgent",
            r"\b(tradingview|chart|technical|rsi)\b": "TradingViewMCPAgent",
            r"\b(ict|smc|order block|liquidity|fvg)\b": "ICTSMCAgent",
            r"\b(risk|drawdown|portfolio)\b": "RiskManager",
            r"\b(wallet|balance)\b": "WalletManager",
        }

    def get_agent_class_name(self, user_input: str) -> str:
        text = user_input.lower().strip()
        for pattern, agent_name in self._routes.items():
            if re.search(pattern, text, re.IGNORECASE):
                return agent_name
        return "GeneralAnalysisAgent"


router = KeywordRouter()