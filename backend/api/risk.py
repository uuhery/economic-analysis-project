from fastapi import APIRouter
from typing import List

from models.risk_model import SensitivityRequest, DecisionPath, MonteCarloRequest
from services.risk_analysis import perform_sensitivity_analysis, perform_decision_tree, perform_monte_carlo_simulation

router = APIRouter(prefix="/risk", tags=["Risk Analysis"])



@router.post("/sensitivity")
def run_sensitivity(req: SensitivityRequest):
    """
    多参数敏感性分析接口，基于 base_context + params 分析 NPV 波动。
    """
    return perform_sensitivity_analysis(req.base_context, req.params)

@router.post("/decision-tree")
def run_decision_tree(paths: List[DecisionPath]):
    """
    接收多条路径（概率+价值），计算期望收益。
    """
    expected_value = perform_decision_tree(paths)
    return {"expected_value": expected_value}


@router.post("/monte-carlo")
def run_monte_carlo(req: MonteCarloRequest):
    """
    执行蒙特卡洛模拟，返回分布数据及统计指标。
    """
    result = perform_monte_carlo_simulation(
        base=req.base,
        std_dev=req.std_dev,
        distribution=req.distribution,
        iterations=req.iterations
    )
    return result