from __future__ import annotations
import re
from typing import Optional
from loguru import logger

class KeywordRouter:
    def __init__(self):
        self._routes = [
            # HIGH PRIORITY - spesifik
            (r"\b(find sol arbitrage|sol arb|jupiter arb)\b", "DEXSpecialist"),
            (r"\b(ict|smc|order block|fvg|liquidity zone)\b", "ICTSMCAgent"),
            (r"\b(rwa|real world asset|ondo|centrifuge)\b", "RWAAgent"),
            (r"\b(execute|place order|trade now)\b", "ExecutionAgent"),
            (r"\b(dlmm|meteora)\b", "DLMMSpecialist"),
            
            # TRADING
            (r"\b(long|short|leverage).*(btc|eth|sol)\b", "FuturesSpecialist"),
            (r"\b(arbitrage|arb).*(sol|jupiter)\b", "ArbitrageAgent"),
            (r"\b(funding rate|funding)\b", "FundingRateAgent"),
            (r"\b(options|call put|gamma)\b", "OptionsAgent"),
            (r"\b(grid bot)\b", "GridBotAgent"),
            (r"\b(uniswap|uni v3)\b", "UniswapAIAgent"),
            (r"\b(forex|eurusd)\b", "ForexSpecialist"),
            (r"\b(stocks|nasdaq)\b", "StocksSpecialist"),
            (r"\b(liquidation|liq cascade)\b", "LiquidationAgent"),
            
            # INTELLIGENCE
            (r"\b(analyze|news|fundamental|catalyst)\b", "IntelligenceResearchAgent"),
            (r"\b(tradingview|chart|technical|rsi|macd)\b", "TradingViewMCPAgent"),
            (r"\b(narrative|sector rotation)\b", "NarrativeAgent"),
            (r"\b(correlation|diversification)\b", "CorrelationAgent"),
            (r"\b(volatility|vol)\b", "VolatilityAgent"),
            (r"\b(prediction market|polymarket)\b", "PredictionMarketAgent"),
            
            # ON-CHAIN
            (r"\b(whale|large transfer)\b", "WhaleAgent"),
            (r"\b(bridge|wormhole)\b", "BridgeAgent"),
            (r"\b(mev|sandwich)\b", "MEVAgent"),
            
            # RISK
            (r"\b(risk|drawdown|position size)\b", "RiskManager"),
            (r"\b(rug|honeypot)\b", "RugAgent"),
            (r"\b(compliance|kyc)\b", "ComplianceAgent"),
            (r"\b(insurance|cover)\b", "InsuranceAgent"),
            
            # WALLET
            (r"\b(wallet|balance|portfolio)\b", "WalletManager"),
            (r"\b(metamask)\b", "MetaMaskAutomation"),
            
            # SPECIALIZED
            (r"\b(airdrop|farm|testnet)\b", "AirdropAgent"),
            (r"\b(nft|bayc|opensea)\b", "NFTAgent"),
            (r"\b(gaming|pixels)\b", "GamingAgent"),
            (r"\b(memecoin|pump)\b", "MemecoinAgent"),
            (r"\b(yield|farming|aave)\b", "DeFiYieldAgent"),
            (r"\b(alpha call)\b", "AlphaMonitor"),
            (r"\b(quest|galxe)\b", "QuestAutomation"),
            (r"\b(macro|fed|dxy)\b", "MacroAgent"),
        ]
    
    def get_agent_class_name(self, user_input: str) -> str:
        text = user_input.lower()
        
        for pattern, agent_name in self._routes:
            if re.search(pattern, text):
                logger.debug(f"Router matched → {agent_name}")
                return agent_name
        
        logger.debug("Router matched → GeneralAnalysisAgent (fallback)")
        return "GeneralAnalysisAgent"

router = KeywordRouter()
