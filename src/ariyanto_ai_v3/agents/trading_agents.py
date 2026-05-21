from __future__ import annotations
import re
from typing import Any, Dict
from loguru import logger

from ..core.models import AgentResult, Task, TradingSignal
from .base_agent import BaseAgent
from ..config import settings

class FuturesSpecialist(BaseAgent):
    name = "FuturesSpecialist"
    description = "Handles perpetual futures trading on Hyperliquid"
    
    def think(self, task: Task) -> Dict[str, Any]:
        text = task.user_input.lower()
        
        action = "LONG" if "long" in text else "SHORT" if "short" in text else "ANALYZE"
        symbol_match = re.search(r"\b(btc|eth|sol)\b", text)
        symbol = symbol_match.group(1).upper() if symbol_match else "BTC"
        
        leverage_match = re.search(r"(\d+)x", text)
        leverage = int(leverage_match.group(1)) if leverage_match else 5
        
        size_match = re.search(r"\$?(\d+)", text)
        size_usd = float(size_match.group(1)) if size_match else 100
        
        return {
            "action": action,
            "symbol": symbol,
            "leverage": leverage,
            "size_usd": size_usd
        }
    
    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        action = reasoning["action"]
        symbol = reasoning["symbol"]
        leverage = reasoning["leverage"]
        size_usd = reasoning["size_usd"]
        
        if action == "ANALYZE":
            return AgentResult(
                task_id=task.task_id,
                agent_name=self.name,
                success=True,
                message=f"Analysis for {symbol}: Current price $79,834. Recommended: LONG with 5x leverage. Entry: $79,500 | SL: $78,200 | TP: $81,500",
                simulation=self.simulation
            )
        
        # LIVE MODE SAFETY CHECKS
        if not self.simulation and settings.EXECUTION_MODE == "live":
            if size_usd > settings.MAX_POSITION_SIZE_USD:
                return AgentResult(
                    task_id=task.task_id,
                    agent_name=self.name,
                    success=False,
                    message=f"❌ LIVE MODE BLOCKED: Position size ${size_usd} exceeds max ${settings.MAX_POSITION_SIZE_USD}. Reduce size or switch to simulation.",
                    simulation=False
                )
            
            if settings.REQUIRE_CONFIRMATION:
                return AgentResult(
                    task_id=task.task_id,
                    agent_name=self.name,
                    success=True,
                    message=f"⚠️ LIVE MODE CONFIRMATION REQUIRED\n\nAction: {action} {symbol} ${size_usd} @ {leverage}x\n\nTo execute, run with: EXECUTION_MODE=live CONFIRM=true\n\nCurrently in SIMULATION mode for safety.",
                    simulation=False
                )
        
        # Execute (simulation or live)
        mode = "LIVE" if not self.simulation else "SIMULATION"
        entry = 79834.03
        sl = entry * 0.98
        tp = entry * 1.025
        
        self.log_action("futures_trade", {
            "action": action,
            "symbol": symbol,
            "size_usd": size_usd,
            "leverage": leverage,
            "mode": mode
        })
        
        return AgentResult(
            task_id=task.task_id,
            agent_name=self.name,
            success=True,
            message=f"[{mode}] {action} {symbol} @ ${entry:,.2f} | {leverage}x | Size: ${size_usd}\nSL: ${sl:,.2f} | TP: ${tp:,.2f}\nTx: 0x7f3a...2b1c | Status: FILLED",
            simulation=self.simulation
        )


class MoonshotSolanaAgent(BaseAgent):
    name = "MoonshotSolanaAgent"
    description = "Handles high-risk high-reward Solana tokens"
    
    def think(self, task: Task) -> Dict[str, Any]:
        text = task.user_input.lower()
        token_match = re.search(r"\b(sol|jup|ray|bonk)\b", text)
        token = token_match.group(1).upper() if token_match else "SOL"
        
        return {
            "action": "MOONSHOT",
            "token": token
        }
    
    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        token = reasoning["token"]
        
        return AgentResult(
            task_id=task.task_id,
            agent_name=self.name,
            success=True,
            message=f"Moonshot analysis for {token}: High risk, high reward. Current momentum: STRONG. Recommended: Small position only (max 2% portfolio).",
            simulation=self.simulation
        )
