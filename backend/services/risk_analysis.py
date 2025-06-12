import numpy as np
from typing import List, Dict
from models.risk_model import SensitivityParam
from pydantic import BaseModel

class SensitivityParam(BaseModel):
    name: str
    min: float
    max: float
    distribution: str = "uniform"

class DecisionPath(BaseModel):
    probability: float
    value: float


def calculate_npv_with_context(context: Dict) -> float:
    """
    给定参数上下文，计算 NPV。
    必须至少包含 cash_flows 和 discount_rate。
    """
    cash_flows = context.get("cash_flows", [])
    discount_rate = context.get("discount_rate", 0.1)
    return round(sum(cf / ((1 + discount_rate) ** t) for t, cf in enumerate(cash_flows)), 2)

def sample_param(param: SensitivityParam, n: int = 200) -> List[float]:
    if param.max == param.min:
        return [param.min] * n
    if param.distribution == "uniform":
        return np.random.uniform(param.min, param.max, n).tolist()
    elif param.distribution == "triangular":
        mid = (param.min + param.max) / 2
        return np.random.triangular(param.min, mid, param.max, n).tolist()
    elif param.distribution == "normal":
        mean = (param.min + param.max) / 2
        std = (param.max - param.min) / 4
        return np.clip(np.random.normal(mean, std, n), param.min, param.max).tolist()
    else:
        return [param.min, param.max]

def perform_sensitivity_analysis(
    base_context: Dict,
    params: List[SensitivityParam],
    samples: int = 200
) -> List[Dict]:
    """
    对 base_context 中每个 param 进行敏感性采样并计算 NPV 分布。
    """
    results = []

    for param in params:
        values = sample_param(param, samples)
        impacts = []

        for v in values:
            context = base_context.copy()
            context[param.name] = v
            npv = calculate_npv_with_context(context)
            impacts.append(npv)

        results.append({
            "param": param.name,
            "min_npv": round(min(impacts), 2),
            "max_npv": round(max(impacts), 2),
            "mean_npv": round(np.mean(impacts), 2),
            "std_npv": round(np.std(impacts), 2)
        })

    return results

def perform_decision_tree(paths: List[DecisionPath]) -> float:
    """
    对路径进行期望值计算：E = Σ(P_i * V_i)
    """
    expected_value = sum(p.probability * p.value for p in paths)
    return round(expected_value, 2)


def perform_monte_carlo_simulation(base: float, std_dev: float, distribution: str, iterations: int) -> Dict:
    """
    执行 Monte Carlo 模拟，根据分布生成随机样本，计算 NPV 分布与统计信息。
    """
    np.random.seed(42)

    if distribution == 'normal':
        samples = np.random.normal(loc=base, scale=std_dev, size=iterations)
    elif distribution == 'triangular':
        samples = np.random.triangular(left=base - std_dev, mode=base, right=base + std_dev, size=iterations)
    else:
        raise ValueError("Unsupported distribution type")

    mean = round(float(np.mean(samples)), 2)
    std = round(float(np.std(samples)), 2)
    min_val = round(float(np.min(samples)), 2)
    max_val = round(float(np.max(samples)), 2)

    loss_prob = round(float(np.mean(samples < 0)), 4)
    high_return_prob = round(float(np.mean(samples > base * 1.2)), 4)

    return {
        "npv_distribution": [round(float(x), 2) for x in samples[:200]],  # 前200点用于画图
        "mean": mean,
        "std_dev": std,
        "min": min_val,
        "max": max_val,
        "loss_probability": loss_prob,
        "high_return_probability": high_return_prob
    }
