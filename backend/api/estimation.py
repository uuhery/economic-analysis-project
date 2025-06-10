from fastapi import APIRouter, HTTPException

from services.estimation_calculator import (
    calculate_expert_judgment,
    calculate_delphi_method, calculate_regression_model, estimate_cocomo, estimate_function_point,
)

from models.estimation_model import (
    CocomoRequest, FunctionPointRequest, ExpertRequest,
    DelphiRequest, RegressionRequest
)
router = APIRouter(prefix="/api/estimation", tags=["Estimation"])

@router.post("/cocomo")
def cocomo_api(data: CocomoRequest):
    try:
        return estimate_cocomo(data.loc, data.mode, data.cost_drivers, data.cost_per_pm)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

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