from pydantic import BaseModel
from typing import List

class SensitivityRequest(BaseModel):
    base_value: float
    variable_range: List[float]
    multiplier: float = 1.0

class DecisionPath(BaseModel):
    probability: float
    value: float

class MonteCarloRequest(BaseModel):
    base: float
    std_dev: float
    iterations: int = 1000