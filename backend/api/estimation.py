from fastapi import APIRouter, HTTPException

from services.estimation_calculator import (calculate_cocomo, calculate_fp, calculate_expert_judgment)
from models.estimation_model import COCOMORequest, FunctionPointRequest, ExpertRequest

router = APIRouter(prefix="/api/estimation", tags=["Estimation"])

# --- 路由定义 ---
@router.post("/cocomo")
def cocomo_api(data: COCOMORequest):
    try:
        effort = calculate_cocomo(data.loc, data.mode)
        return {"effort_person_months": effort}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/function_points")
def function_points_api(data: FunctionPointRequest):
    result = calculate_fp(data.dict())
    return result

@router.post("/expert")
def expert_api(data: ExpertRequest):
    try:
        result = calculate_expert_judgment(data.estimates)
        return {"average_estimate": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
