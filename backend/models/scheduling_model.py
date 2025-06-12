from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    name: str
    duration: int
    deadline: int
    priority: Optional[int] = 1  # 默认优先级为 1（最低）
    earliest_start: Optional[int] = 0  # 默认最早开始时间为 0

class ResourceTask(BaseModel):
    name: str
    workload: float
    flexibility: Optional[int] = 0  # 最大可延迟时间（默认不延迟）

class BalanceInput(BaseModel):
    tasks: List[ResourceTask]
    total_resources: float
    total_time: int