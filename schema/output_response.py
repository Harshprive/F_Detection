from pydantic import BaseModel, Field
from typing import Literal, List
from datetime import datetime

class RiskResponse(BaseModel):
    payment_risk_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Fraud probability scaled from 0 to 100"
    )

    risk_level: Literal["LOW", "MEDIUM", "HIGH"]

    recommended_action: Literal[
        "ALLOW",
        "STEP_UP_AUTH",
        "BLOCK"
    ]

    confidence_score: float = Field(
        ...,
        ge=0,
        le=1,
        description="Model confidence in the decision"
    )

    model_version: str = Field(
        ...,
        description="Deployed model version"
    )

    evaluated_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    triggered_rules: List[str] = Field(
        default_factory=list,
        description="Heuristic rules triggered in addition to ML"
    )
