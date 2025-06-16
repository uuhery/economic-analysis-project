from typing import List

from fastapi import APIRouter, HTTPException

from models.finance_model import CashFlowModel, ROIModel, EstimatesModel, BudgetModel

from services.finance_calculator import (
    calculate_npv, calculate_roi, calculate_irr, calculate_payback, track_budget, forecast_next_phase, analyze_variance
)

router = APIRouter(prefix="/finance", tags=["Finance"])

# NPV
@router.post("/npv")
def npv(data: CashFlowModel):
    try:
        result = calculate_npv(data.cash_flows, data.discount_rate)
        return {"npv": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ROI
@router.post("/roi")
def roi(data: ROIModel):
    try:
        result = calculate_roi(data.gain, data.cost)
        return {"roi_percent": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# IRR
@router.post("/irr")
def irr(data: EstimatesModel):
    try:
        result = calculate_irr(data.cash_flows)
        return {"irr_percent": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Payback
@router.post("/payback")
def payback(data: EstimatesModel):
    try:
        result = calculate_payback(data.cash_flows)
        if result == -1:
            return {"payback_period": None, "message": "Investment never recovered"}
        return {"payback_period": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Budget-tracking
@router.post("/budget-tracking")
def budget_tracking(data: List[BudgetModel]):
    try:
        raw_data = [item.dict() for item in data]
        result = track_budget(raw_data)
        return {"tracked": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Variance Analysis
@router.post("/variance-analysis")
def variance_analysis(data: List[BudgetModel]):
    try:
        raw_data = [item.dict() for item in data]
        result = analyze_variance(raw_data)
        return {"analysis": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Forecast
@router.post("/forecast")
def forecast(data: List[BudgetModel]):
    try:
        raw_data = [item.dict() for item in data]
        result = forecast_next_phase(raw_data)
        return {"forecast": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))