from pydantic import BaseModel, Field
from typing import List, Dict, Any


class SensitivityParam(BaseModel):
    name: str
    min: float
    max: float
    distribution: str = "uniform"  # 'uniform', 'triangular', 'normal'

class SensitivityRequest(BaseModel):
    base_context: Dict[str, Any]  # 包括 cash_flows, discount_rate 等上下文
    params: List[SensitivityParam]

class DecisionPath(BaseModel):
    probability: float = Field(..., ge=0.0, le=1.0, example=0.6)
    value: float = Field(..., example=100000)

class MonteCarloRequest(BaseModel):
    base: float = Field(..., example=1000)
    std_dev: float = Field(..., example=250)
    distribution: str = Field(..., example="normal")
    iterations: int = Field(..., gt=0, example=1000)