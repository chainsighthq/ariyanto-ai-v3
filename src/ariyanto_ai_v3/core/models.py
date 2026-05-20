from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Literal
from uuid import uuid4

from pydantic import BaseModel, Field, ConfigDict, field_validator


class TaskType(str, Enum):
    TRADING = "trading"
    INTELLIGENCE = "intelligence"
    ONCHAIN = "onchain"
    RISK = "risk"
    WALLET = "wallet"
    SPECIALIZED = "specialized"
    GENERAL = "general"


class ExecutionMode(str, Enum):
    SIMULATION = "simulation"
    LIVE = "live"


class Task(BaseModel):
    model_config = ConfigDict(extra="ignore")
    task_id: str = Field(default_factory=lambda: str(uuid4()))
    user_input: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source: Literal["telegram", "cli", "api", "internal"] = "cli"
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("user_input")
    @classmethod
    def validate_user_input(cls, v: str) -> str:
        if not v or len(v.strip()) < 3:
            raise ValueError("user_input must be at least 3 characters")
        return v.strip()


class AgentResult(BaseModel):
    model_config = ConfigDict(extra="ignore")
    task_id: str
    agent_name: str
    success: bool
    result_data: Dict[str, Any] = Field(default_factory=dict)
    message: str = ""
    alerts: List[str] = Field(default_factory=list)
    execution_time_ms: Optional[float] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    error: Optional[str] = None
    simulation: bool = True


class RiskMetrics(BaseModel):
    portfolio_value: float
    drawdown_percent: float
    open_positions_value: float = 0.0
    risk_score: float = Field(ge=0, le=100, default=50.0)
    max_drawdown_allowed: float = 3.0
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))