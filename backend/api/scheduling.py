from fastapi import APIRouter
from typing import List

from models.scheduling_model import Task, BalanceInput
from services.scheduling_calculator import greedy_schedule, resource_smoothing

router = APIRouter(prefix="/api/scheduling")

@router.post("/optimize")
def optimize_schedule(tasks: List[Task]):
    result = greedy_schedule([t.dict() for t in tasks])
    return {"schedule": result}


@router.post("/smooth")
def smooth_resources(data: BalanceInput):
    result = resource_smoothing(
        [t.dict() for t in data.tasks],
        data.total_resources,
        data.total_time
    )
    return {"allocation": result}
