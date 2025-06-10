from pydantic import BaseModel
from typing import List
# 通用模型
class CashFlowModel(BaseModel):
    cash_flows: List[float]
    discount_rate: float = 0.1

class ROIModel(BaseModel):
    gain: float
    cost: float

class EstimatesModel(BaseModel):
    cash_flows: List[float]