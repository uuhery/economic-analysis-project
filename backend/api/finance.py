from fastapi import APIRouter, HTTPException

from models.finance_model import CashFlowModel, ROIModel, EstimatesModel

from services.finance_calculator import (
    calculate_npv, calculate_roi, calculate_irr, calculate_payback
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
