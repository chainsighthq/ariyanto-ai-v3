"""
Prometheus Metrics for ARIYANTO AI v3
"""

from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
from functools import wraps

# Metrics
TASKS_PROCESSED = Counter(
    'ariyanto_tasks_total',
    'Total number of tasks processed',
    ['agent_name', 'status']
)

TASK_DURATION = Histogram(
    'ariyanto_task_duration_seconds',
    'Task processing duration in seconds',
    ['agent_name']
)

ACTIVE_AGENTS = Gauge(
    'ariyanto_active_agents',
    'Number of currently active agents'
)

REDIS_OPERATIONS = Counter(
    'ariyanto_redis_operations_total',
    'Total Redis operations',
    ['operation', 'status']
)

SQLITE_OPERATIONS = Counter(
    'ariyanto_sqlite_operations_total',
    'Total SQLite operations',
    ['operation', 'status']
)

LIVE_TRADES = Counter(
    'ariyanto_live_trades_total',
    'Total live trades executed',
    ['symbol', 'action']
)

def track_task(agent_name: str):
    """Decorator to track task metrics"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                status = "success" if result.success else "error"
                TASKS_PROCESSED.labels(agent_name=agent_name, status=status).inc()
                return result
            finally:
                duration = time.time() - start_time
                TASK_DURATION.labels(agent_name=agent_name).observe(duration)
        return wrapper
    return decorator

def start_metrics_server(port: int = 8000):
    """Start Prometheus metrics HTTP server"""
    start_http_server(port)
    print(f"📊 Prometheus metrics available at http://localhost:{port}/metrics")
