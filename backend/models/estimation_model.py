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

class ExpertEntry(BaseModel):
    name: str = None
    estimate: float
    confidence: float  # 0 ~ 1

class ExpertRequest(BaseModel):
    experts: List[ExpertEntry]

class DelphiRequest(BaseModel):
    rounds: List[List[float]]
    convergence_threshold: float = 5.0  # 可选字段，默认值为5

class RegressionRequest(BaseModel):
    data: List[List[float]]  # [[x, y], [x, y], ...]
    predict_x: float