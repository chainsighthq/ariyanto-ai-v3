from __future__ import annotations
from typing import Dict, Any
from loguru import logger

from ..core.models import AgentResult, Task
from .base_agent import BaseAgent
from ..utils.exchange_connector import HyperliquidConnector

class ExecutionAgent(BaseAgent):
    name = "ExecutionAgent"
    description = "Handles order execution (simulation + live ready)"
    
    def __init__(self, memory_manager=None, simulation: bool = True):
        super().__init__(memory_manager, simulation)
        self.connector = HyperliquidConnector(simulation=simulation)
    
    def think(self, task: Task) -> Dict[str, Any]:
        text = task.user_input.lower()
        
        # Simple parsing
        if "long" in text or "buy" in text:
            action = "LONG"
        elif "short" in text or "sell" in text:
            action = "SHORT"
        else:
            action = "UNKNOWN"
        
        # Extract symbol (simple)
        symbol = "BTC"
        for s in ["eth", "sol", "btc"]:
            if s in text:
                symbol = s.upper()
                break
        
        return {
            "action": action,
            "symbol": f"{symbol}USDT",
            "raw_input": task.user_input
        }
    
    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        action = reasoning["action"]
        symbol = reasoning["symbol"]
        
        if action == "UNKNOWN":
            return AgentResult(
                task_id=task.task_id,
                agent_name=self.name,
                success=False,
                message="Could not understand order. Use: 'Long BTC', 'Short ETH', etc.",
                simulation=self.simulation
            )
        
        # Get current price
        price = self.connector.get_price(symbol.replace("USDT", ""))
        
        # Place order (simulation)
        order_result = self.connector.place_order(
            symbol=symbol,
            side=action,
            size=0.01,           # small size for safety
            leverage=10
        )
        
        msg = (
            f"{'[SIM]' if self.simulation else '[LIVE]'} "
            f"{action} {symbol} @ ${price:,.2f}\n"
            f"Order ID: {order_result.get('order_id', 'N/A')}\n"
            f"Status: {order_result.get('status', 'UNKNOWN')}"
        )
        
        return AgentResult(
            task_id=task.task_id,
            agent_name=self.name,
            success=True,
            message=msg,
            result_data={"order": order_result},
            simulation=self.simulation
        )
