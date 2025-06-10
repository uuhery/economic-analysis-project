from pydantic import BaseModel
from typing import List

class NPVRequest(BaseModel):
    cash_flows: List[float]
    discount_rate: float = 0.1  # 默认折现率 10%
