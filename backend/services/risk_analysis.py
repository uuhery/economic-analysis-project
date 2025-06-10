import numpy as np
import random

def sensitivity_analysis(base_value: float, variable_range: list[float], multiplier: float = 1.0):
    results = []
    for v in variable_range:
        impact = (v * multiplier) - base_value
        results.append(round(impact, 2))
    return {
        "labels": variable_range,
        "impact": results
    }


def decision_tree_analysis(paths: list[dict]):
    """
    每个 path: { "probability": 0.3, "value": 1000 }
    返回期望值
    """
    expected_value = sum(p["probability"] * p["value"] for p in paths)
    return round(expected_value, 2)


def monte_carlo_simulation(base: float, std_dev: float, iterations: int = 1000):
    """
    用正态分布模拟 base 的波动
    """
    results = np.random.normal(loc=base, scale=std_dev, size=iterations)
    mean_result = np.mean(results)
    return {
        "mean": round(mean_result, 2),
        "min": round(np.min(results), 2),
        "max": round(np.max(results), 2),
        "std_dev": round(np.std(results), 2)
    }
