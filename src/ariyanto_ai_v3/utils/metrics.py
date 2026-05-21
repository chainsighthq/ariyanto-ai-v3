from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
from functools import wraps

# Metrics
TASKS_PROCESSED = Counter('ariyanto_tasks_total', 'Total tasks processed', ['agent', 'status'])
TASK_DURATION = Histogram('ariyanto_task_duration_seconds', 'Task processing time')
ACTIVE_AGENTS = Gauge('ariyanto_active_agents', 'Currently active agents')
LIVE_TRADES = Counter('ariyanto_live_trades_total', 'Live trades executed')

def track_task(agent_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                TASKS_PROCESSED.labels(agent=agent_name, status='success').inc()
                return result
            except Exception:
                TASKS_PROCESSED.labels(agent=agent_name, status='error').inc()
                raise
            finally:
                TASK_DURATION.observe(time.time() - start)
        return wrapper
    return decorator

def start_metrics_server(port: int = 8000):
    start_http_server(port)
    print(f"📊 Prometheus metrics started on port {port}")
