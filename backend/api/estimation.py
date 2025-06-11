from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import pandas as pd
import io

from services.estimation_calculator import (
    calculate_expert_judgment,
    calculate_delphi_method, calculate_regression_model, estimate_cocomo, estimate_function_point,
)

from models.estimation_model import (
    CocomoRequest, FunctionPointRequest, ExpertRequest,
    DelphiRequest, RegressionRequest
)
router = APIRouter(prefix="/estimation", tags=["Estimation"])

@router.post("/cocomo")
def cocomo_api(data: CocomoRequest):
    try:
        return estimate_cocomo(data.loc, data.mode, data.cost_drivers, data.cost_per_pm)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/function_points")
def function_points_api(data: FunctionPointRequest):
    try:
        return estimate_function_point(
            data.fp_inputs,
            data.fp_weights,
            data.language,
            data.cost_drivers
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/expert")
def expert_api(data: ExpertRequest):
    try:
        result = calculate_expert_judgment([e.dict() for e in data.experts])
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/delphi")
def delphi_api(data: DelphiRequest):
    try:
        result = calculate_delphi_method(data.rounds, data.convergence_threshold)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/regression")
async def regression_from_file(
    file: UploadFile = File(...),
    x_column: str = Form(...),
    y_column: str = Form(...),
    predict_x: float = Form(...)
):
    try:
        content = await file.read()
        # 自动处理编码（只对 CSV）
        if file.filename.endswith(".csv"):
            df = safe_read_csv(content)
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format.")

        # 验证列存在
        if x_column not in df.columns or y_column not in df.columns:
            raise HTTPException(status_code=400, detail="Selected columns not found.")

        inputs = df[[x_column, y_column]].dropna().values.tolist()
        result = calculate_regression_model(inputs, predict_x)

        return {
            "regression_formula": f"y = {result['slope_b']}x + {result['intercept_a']}",
            "intercept_a": result["intercept_a"],
            "slope_b": result["slope_b"],
            "predict_x": predict_x,
            "predict_y": result["predict_y"],
            "sample_count": result["sample_count"],
            "r_squared": result["r_squared"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def safe_read_csv(content: bytes) -> pd.DataFrame:
    for enc in ['utf-8', 'gbk', 'ISO-8859-1']:
        try:
            return pd.read_csv(io.BytesIO(content), encoding=enc)
        except UnicodeDecodeError:
            continue
    raise ValueError("Unable to decode CSV. Please save as UTF-8 encoding.")