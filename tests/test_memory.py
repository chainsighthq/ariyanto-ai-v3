import pytest
import tempfile
import os
from src.ariyanto_ai_v3.memory.sqlite_memory import SQLiteMemory

class TestSQLiteMemory:
    
    @pytest.fixture
    def memory(self):
        # Use temporary database for testing
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        
        mem = SQLiteMemory(db_path=db_path)
        yield mem
        
        # Cleanup
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    def test_set_and_get_agent_state(self, memory):
        memory.set_agent_state("TestAgent", {"key": "value", "number": 42})
        state = memory.get_agent_state("TestAgent")
        
        assert state is not None
        assert state["key"] == "value"
        assert state["number"] == 42
    
    def test_log_audit(self, memory):
        memory.log_audit(
            agent_name="TestAgent",
            action="test_action",
            details={"test": True},
            correlation_id="test-123",
            simulation=True
        )
        
        # Should not raise any exception
        assert True
