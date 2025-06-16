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

class BudgetModel(BaseModel):
    phase: str  # 项目阶段（如“设计阶段”、“开发阶段”）
    budgeted_amount: float  # 预算金额
    actual_amount: float  # 实际金额