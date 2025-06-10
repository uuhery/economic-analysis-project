from fastapi import APIRouter, HTTPException
from models.npv_model import NPVRequest
from services.npv import calculate_npv

router = APIRouter()

@router.post("/npv")
def npv_endpoint(data: NPVRequest):
    if not data.cash_flows:
        raise HTTPException(status_code=400, detail="cash_flows must be non-empty")

    try:
        result = calculate_npv(data.cash_flows, data.discount_rate)
        return {"npv": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
