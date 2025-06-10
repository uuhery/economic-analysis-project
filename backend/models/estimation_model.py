from typing import Optional, List, Tuple, Dict
from pydantic import BaseModel

# 使用前端配置的权重计算
class FunctionPointRequest(BaseModel):
    fp_inputs: Dict[str, int]
    fp_weights: Dict[str, float]
    language: str
    cost_drivers: Dict[str, float]

class CocomoRequest(BaseModel):
    loc: float
    mode: str
    cost_drivers: Dict[str, str]
    cost_per_pm: float  # 每人月成本（例如：￥10,000）

class ExpertRequest(BaseModel):
    estimates: List[float]

class DelphiRequest(BaseModel):
    rounds: List[List[float]]

class RegressionRequest(BaseModel):
    data: List[Tuple[float, float]]