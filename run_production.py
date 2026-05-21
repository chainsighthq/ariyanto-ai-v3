#!/usr/bin/env python3
"""
ARIYANTO AI v3 - Production Runner with Prometheus Metrics
"""

import os
import sys
import time
import signal
from pathlib import Path
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent / "src"))

from ariyanto_ai_v3.agents.supervisor_agent import SupervisorAgent
from ariyanto_ai_v3.core.models import Task
from ariyanto_ai_v3.config import settings
from ariyanto_ai_v3.utils.telegram_notifier import TelegramNotifier
from ariyanto_ai_v3.utils.metrics import start_metrics_server, TASKS_PROCESSED

# Configure logging
logger.remove()
logger.add(sys.stdout, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}")
logger.add("logs/production.log", rotation="100 MB", retention="30 days", level="DEBUG")

class ProductionRunner:
    def __init__(self):
        self.running = True
        self.supervisor = SupervisorAgent(simulation=(settings.EXECUTION_MODE == "simulation"))
        self.notifier = TelegramNotifier()
        
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        
        mode = "🔴 LIVE" if settings.EXECUTION_MODE == "live" else "🟢 SIMULATION"
        logger.warning(f"Starting ARIYANTO AI v3 in {mode} mode")
        
        # Start Prometheus metrics server
        start_metrics_server(port=8000)
        
        if settings.EXECUTION_MODE == "live":
            logger.critical("⚠️ LIVE TRADING MODE ENABLED!")
            self.notifier.send_sync("⚠️ ARIYANTO AI v3 started in LIVE mode!")
    
    def shutdown(self, signum, frame):
        logger.info("Shutdown signal received")
        self.running = False
    
    def run_monitoring_loop(self):
        logger.info("Production monitoring loop started (every 5 min)")
        
        while self.running:
            try:
                # Monitor funding rates
                task = Task(user_input="Check BTC funding rate", source="internal")
                result = self.supervisor.run(task)
                
                TASKS_PROCESSED.labels(
                    agent_name=result.result_data.get("routed_to", "unknown"),
                    status="success" if result.success else "error"
                ).inc()
                
                if result.success:
                    logger.info(f"✓ {result.message[:60]}...")
                
                time.sleep(300)  # 5 minutes
                
            except Exception as e:
                logger.error(f"Error: {e}")
                time.sleep(60)
        
        logger.info("Production runner stopped")

if __name__ == "__main__":
    runner = ProductionRunner()
    runner.run_monitoring_loop()
