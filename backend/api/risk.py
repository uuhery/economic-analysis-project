from fastapi import APIRouter
from typing import List

from models.risk_model import SensitivityRequest, DecisionPath, MonteCarloRequest
from services.risk_analysis import sensitivity_analysis, decision_tree_analysis, monte_carlo_simulation

router = APIRouter(prefix="/api/risk", tags=["Risk Analysis"])


@router.post("/sensitivity")
def run_sensitivity(req: SensitivityRequest):
    result = sensitivity_analysis(req.base_value, req.variable_range, req.multiplier)
    return {"impact": result}

@router.post("/decision-tree")
def run_decision_tree(paths: List[DecisionPath]):
    result = decision_tree_analysis([p.dict() for p in paths])
    return {"expected_value": result}

@router.post("/monte-carlo")
def run_monte_carlo(req: MonteCarloRequest):
    result = monte_carlo_simulation(req.base, req.std_dev, req.iterations)
    return result
