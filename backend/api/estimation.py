from fastapi import APIRouter, HTTPException

from services.estimation_calculator import (
    calculate_cocomo, calculate_fp, calculate_expert_judgment,
    calculate_delphi_method, calculate_regression_model
)

from models.estimation_model import (
    COCOMORequest, FunctionPointRequest, ExpertRequest,
    DelphiRequest, RegressionRequest
)
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


@router.post("/delphi")
def delphi_api(data: DelphiRequest):
    try:
        result = calculate_delphi_method(data.rounds)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/regression")
def regression_api(data: RegressionRequest):
    try:
        result = calculate_regression_model(data.data)
        # 函数 predict_function 不能直接返回，改为说明格式
        return {
            "intercept_a": result["intercept_a"],
            "slope_b": result["slope_b"],
            "sample_count": result["sample_count"],
            "predict_example_x=100": result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))