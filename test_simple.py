import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

# Test langsung tanpa import agent
from ariyanto_ai_v3.core.models import Task
from ariyanto_ai_v3.core.router import router

# Test router saja
print("Testing Router...")
print("Find SOL arbitrage ->", router.get_agent_class_name("Find SOL arbitrage"))
print("Long BTC 10x ->", router.get_agent_class_name("Long BTC 10x"))
print("Analyze XAGUSD with ICT ->", router.get_agent_class_name("Analyze XAGUSD with ICT"))
print("Check portfolio risk ->", router.get_agent_class_name("Check portfolio risk"))
