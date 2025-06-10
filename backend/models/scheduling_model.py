from pydantic import BaseModel
from typing import List

class Task(BaseModel):
    name: str
    duration: int
    deadline: int

class ResourceTask(BaseModel):
    name: str
    workload: float

class BalanceInput(BaseModel):
    tasks: List[ResourceTask]
    total_resources: float
    total_time: int
