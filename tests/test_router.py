import pytest
from src.ariyanto_ai_v3.core.router import router

class TestKeywordRouter:
    
    def test_futures_routing(self):
        assert router.get_agent_class_name("Long BTC 10x") == "FuturesSpecialist"
        assert router.get_agent_class_name("Short ETH 5x") == "FuturesSpecialist"
    
    def test_risk_routing(self):
        assert router.get_agent_class_name("Check portfolio risk") == "RiskManager"
        assert router.get_agent_class_name("Drawdown breach") == "RiskManager"
    
    def test_ict_routing(self):
        assert router.get_agent_class_name("Analyze XAGUSD with ICT") == "ICTSMCAgent"
        assert router.get_agent_class_name("Order block liquidity") == "ICTSMCAgent"
    
    def test_dex_routing(self):
        assert router.get_agent_class_name("Find SOL arbitrage") == "DEXSpecialist"
    
    def test_fallback(self):
        assert router.get_agent_class_name("Random unrelated task") == "GeneralAnalysisAgent"
    
    def test_live_trading_routing(self):
        assert router.get_agent_class_name("Execute my BTC trade") == "ExecutionAgent"
    
    def test_rwa_routing(self):
        assert router.get_agent_class_name("RWA investment options") == "RWAAgent"
