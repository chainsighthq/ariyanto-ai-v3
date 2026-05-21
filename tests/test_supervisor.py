import pytest
from src.ariyanto_ai_v3.agents.supervisor_agent import SupervisorAgent
from src.ariyanto_ai_v3.core.models import Task

class TestSupervisorAgent:
    
    @pytest.fixture
    def supervisor(self):
        return SupervisorAgent(simulation=True)
    
    def test_routing_to_futures(self, supervisor):
        task = Task(user_input="Long BTC 10x", source="cli")
        result = supervisor.run(task)
        assert result.success is True
        assert result.result_data.get("routed_to") == "FuturesSpecialist"
    
    def test_routing_to_risk(self, supervisor):
        task = Task(user_input="Check portfolio risk", source="cli")
        result = supervisor.run(task)
        assert result.success is True
        assert result.result_data.get("routed_to") == "RiskManager"
    
    def test_routing_to_dex(self, supervisor):
        task = Task(user_input="Find SOL arbitrage", source="cli")
        result = supervisor.run(task)
        assert result.success is True
        # Sekarang diarahkan ke DEXSpecialist (lebih spesifik)
        assert result.result_data.get("routed_to") == "DEXSpecialist"
    
    def test_graceful_degradation(self, supervisor):
        task = Task(user_input="xyz123 random nonsense", source="cli")
        result = supervisor.run(task)
        assert result is not None
