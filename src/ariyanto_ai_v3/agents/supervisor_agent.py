from __future__ import annotations
from typing import Any, Dict, Optional
from loguru import logger

from ..core.models import AgentResult, Task
from ..core.router import router
from ..memory import MemoryManager
from .base_agent import BaseAgent

from ariyanto_ai_v3.agents.trading_agents import FuturesSpecialist, MoonshotSolanaAgent
from ariyanto_ai_v3.agents.intelligence_agents import IntelligenceResearchAgent, TradingViewMCPAgent
from ariyanto_ai_v3.agents.onchain_agents import ICTSMCAgent
from ariyanto_ai_v3.agents.risk_agents import RiskManager
from ariyanto_ai_v3.agents.wallet_agents import WalletManager
from ariyanto_ai_v3.agents.specialized_agents import GeneralAnalysisAgent
from ariyanto_ai_v3.agents.dex_agent import DEXSpecialist
from ariyanto_ai_v3.agents.whale_agent import WhaleAgent
from ariyanto_ai_v3.agents.macro_agent import MacroAgent
from ariyanto_ai_v3.agents.airdrop_agent import AirdropAgent
from ariyanto_ai_v3.agents.sentiment_agent import SentimentAgent
from ariyanto_ai_v3.agents.tge_agent import TGEAgent
from ariyanto_ai_v3.agents.rug_agent import RugAgent
from ariyanto_ai_v3.agents.arbitrage_agent import ArbitrageAgent
from ariyanto_ai_v3.agents.funding_agent import FundingRateAgent
from ariyanto_ai_v3.agents.options_agent import OptionsAgent
from ariyanto_ai_v3.agents.narrative_agent import NarrativeAgent
from ariyanto_ai_v3.agents.spot_agent import SpotTradingAgent
from ariyanto_ai_v3.agents.dca_agent import DCAAgent
from ariyanto_ai_v3.agents.compliance_agent import ComplianceAgent
from ariyanto_ai_v3.agents.insurance_agent import InsuranceAgent
from ariyanto_ai_v3.agents.bridge_agent import BridgeAgent
from ariyanto_ai_v3.agents.mev_agent import MEVAgent
from ariyanto_ai_v3.agents.social_agent import SocialMediaAgent
from ariyanto_ai_v3.agents.news_agent import NewsAggregatorAgent
from ariyanto_ai_v3.agents.yield_agent import YieldFarmingAgent
from ariyanto_ai_v3.agents.rwa_agent import RWAAgent
from ariyanto_ai_v3.agents.gaming_agent import GamingAgent
from ariyanto_ai_v3.agents.memecoin_agent import MemecoinAgent
from ariyanto_ai_v3.agents.liquidation_agent import LiquidationAgent
from ariyanto_ai_v3.agents.correlation_agent import CorrelationAgent
from ariyanto_ai_v3.agents.volatility_agent import VolatilityAgent
from ariyanto_ai_v3.agents.portfolio_agent import PortfolioOptimizerAgent
from ariyanto_ai_v3.agents.execution_agent import ExecutionAgent
from ariyanto_ai_v3.agents.dlmm_agent import DLMMSpecialist
from ariyanto_ai_v3.agents.uniswap_agent import UniswapAIAgent
from ariyanto_ai_v3.agents.prediction_agent import PredictionMarketAgent
from ariyanto_ai_v3.agents.chart_agent import ChartScreenshotAgent
from ariyanto_ai_v3.agents.audit_agent import AuditLogger
from ariyanto_ai_v3.agents.secure_wallet_agent import SecureWalletManager
from ariyanto_ai_v3.agents.metamask_agent import MetaMaskAutomation
from ariyanto_ai_v3.agents.trade_executor_agent import TradeExecutor
from ariyanto_ai_v3.agents.forex_agent import ForexSpecialist
from ariyanto_ai_v3.agents.stocks_agent import StocksSpecialist
from ariyanto_ai_v3.agents.alpha_agent import AlphaMonitor
from ariyanto_ai_v3.agents.quest_agent import QuestAutomation
from ariyanto_ai_v3.agents.nft_fcfs_agent import NFTFCFSSpecialist

class SupervisorAgent(BaseAgent):
    name = "SupervisorAgent"
    tier = 1
    description = "Main Orchestrator"

    def __init__(self, memory_manager: Optional[MemoryManager] = None, simulation: bool = True):
        super().__init__(memory_manager, simulation)
        self._agent_registry = {
            "FuturesSpecialist": FuturesSpecialist,
            "MoonshotSolanaAgent": MoonshotSolanaAgent,
            "IntelligenceResearchAgent": IntelligenceResearchAgent,
            "TradingViewMCPAgent": TradingViewMCPAgent,
            "ICTSMCAgent": ICTSMCAgent,
            "RiskManager": RiskManager,
            "WalletManager": WalletManager,
            "GeneralAnalysisAgent": GeneralAnalysisAgent,
            "DEXSpecialist": DEXSpecialist,
            "WhaleAgent": WhaleAgent,
            "MacroAgent": MacroAgent,
            "AirdropAgent": AirdropAgent,
            "SentimentAgent": SentimentAgent,
            "TGEAgent": TGEAgent,
            "RugAgent": RugAgent,
            "ArbitrageAgent": ArbitrageAgent,
            "FundingRateAgent": FundingRateAgent,
            "OptionsAgent": OptionsAgent,
            "NarrativeAgent": NarrativeAgent,
            "SpotTradingAgent": SpotTradingAgent,
            "DCAAgent": DCAAgent,
            "ComplianceAgent": ComplianceAgent,
            "InsuranceAgent": InsuranceAgent,
            "BridgeAgent": BridgeAgent,
            "MEVAgent": MEVAgent,
            "SocialMediaAgent": SocialMediaAgent,
            "NewsAggregatorAgent": NewsAggregatorAgent,
            "YieldFarmingAgent": YieldFarmingAgent,
            "RWAAgent": RWAAgent,
            "GamingAgent": GamingAgent,
            "MemecoinAgent": MemecoinAgent,
            "LiquidationAgent": LiquidationAgent,
            "CorrelationAgent": CorrelationAgent,
            "VolatilityAgent": VolatilityAgent,
            "PortfolioOptimizerAgent": PortfolioOptimizerAgent,
            "ExecutionAgent": ExecutionAgent,
            "DLMMSpecialist": DLMMSpecialist,
            "UniswapAIAgent": UniswapAIAgent,
            "PredictionMarketAgent": PredictionMarketAgent,
            "ChartScreenshotAgent": ChartScreenshotAgent,
            "AuditLogger": AuditLogger,
            "SecureWalletManager": SecureWalletManager,
            "MetaMaskAutomation": MetaMaskAutomation,
            "TradeExecutor": TradeExecutor,
            "ForexSpecialist": ForexSpecialist,
            "StocksSpecialist": StocksSpecialist,
            "AlphaMonitor": AlphaMonitor,
            "QuestAutomation": QuestAutomation,
            "NFTFCFSSpecialist": NFTFCFSSpecialist,
        }

    def think(self, task: Task) -> Dict[str, Any]:
        agent_name = router.get_agent_class_name(task.user_input)
        return {"routed_to": agent_name, "original_input": task.user_input}

    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        agent_name = reasoning.get("routed_to", "GeneralAnalysisAgent")
        AgentClass = self._agent_registry.get(agent_name, GeneralAnalysisAgent)
        try:
            specialist = AgentClass(memory_manager=self.memory, simulation=self.simulation)
            specialist_result = specialist.run(task)
            return AgentResult(task_id=task.task_id, agent_name=self.name, success=specialist_result.success, result_data={"routed_to": agent_name}, message=f"Delegated to {agent_name}. {specialist_result.message}", alerts=specialist_result.alerts, simulation=self.simulation)
        except Exception as e:
            logger.error(f"Delegation failed: {e}")
            return AgentResult(task_id=task.task_id, agent_name=self.name, success=False, message=f"Error: {str(e)}", simulation=self.simulation)
