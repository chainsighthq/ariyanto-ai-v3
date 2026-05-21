import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from ariyanto_ai_v3.agents.supervisor_agent import SupervisorAgent
from ariyanto_ai_v3.core.models import Task
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py \"Your task here\"")
        print("Example: python run.py \"Long BTC 10x\"")
        return

    user_input = " ".join(sys.argv[1:])
    supervisor = SupervisorAgent(simulation=True)
    task = Task(user_input=user_input, source="cli")

    print(f"\n{'='*60}")
    print(f"ARIYANTO AI v3 | {user_input}")
    print(f"{'='*60}\n")

    result = supervisor.run(task)
    print(f"Routed to : {result.result_data.get('routed_to')}")
    print(f"Success   : {result.success}")
    print(f"Message   : {result.message}")

if __name__ == "__main__":
    main()
