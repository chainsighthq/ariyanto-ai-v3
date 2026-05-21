from __future__ import annotations
import re
from typing import Any, Dict
from ..core.models import AgentResult, Task
from .base_agent import BaseAgent


class DEXSpecialist(BaseAgent):
    name = "DEXSpecialist"
    description = "Solana DEX arbitrage & best route finder (Jupiter style)"

    def think(self, task: Task) -> Dict[str, Any]:
        text = task.user_input.lower()
        # Ekstrak token jika ada
        token_match = re.search(r"\b(sol|usdc|usdt|jup|bonk)\b", text)
        token = token_match.group(1).upper() if token_match else "SOL"
        return {
            "type": "arbitrage" if "arbitrage" in text or "arb" in text else "route",
            "token": token
        }

    def act(self, reasoning: Dict[str, Any], task: Task) -> AgentResult:
        token = reasoning.get("token", "SOL")

        if reasoning.get("type") == "arbitrage":
            return AgentResult(
                task_id=task.task_id,
                agent_name=self.name,
                success=True,
                message=f"Arbitrage check for {token}: Best opportunity ~0.31% (Raydium → Orca)",
                result_data={"profit_pct": 0.31, "route": "Raydium → Orca"},
                simulation=self.simulation,
            )

        # Default: best route simulation
        return AgentResult(
            task_id=task.task_id,
            agent_name=self.name,
            success=True,
            message=f"Best route for {token}: Jupiter aggregated route ready (simulated)",
            result_data={"best_dex": "Jupiter", "estimated_slippage": "0.12%"},
            simulation=self.simulation,
        )
