import math
from typing import Dict, List

LANGUAGE_FP_TO_KLOC = {
    'java': 53,
    'python': 42,
    'c++': 55,
    'javascript': 54,
    'cobol': 80
}

def estimate_function_point(fp_inputs: Dict[str, int],
                            fp_weights: Dict[str, float],
                            language: str,
                            cost_drivers: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    raw_fp = sum(fp_inputs[k] * fp_weights.get(k, 0) for k in fp_weights)
    vaf = calculate_vaf(cost_drivers)
    adjusted_fp = raw_fp * vaf

    if language not in LANGUAGE_FP_TO_KLOC:
        raise ValueError(f"Unsupported language '{language}'")

    kloc = adjusted_fp * LANGUAGE_FP_TO_KLOC[language] / 1000.0

    return {
        "raw_fp": round(raw_fp, 2),
        "vaf": round(vaf, 2),
        "adjusted_fp": round(adjusted_fp, 2),
        "kloc": round(kloc, 3)
    }

def calculate_vaf(cost_drivers: Dict[str, float]) -> float:
    total = sum(cost_drivers.values())
    return 0.65 + 0.01 * total

EAF_TABLE = {
    "RELY": {"Very Low": 0.75, "Low": 0.88, "Nominal": 1.00, "High": 1.15, "Very High": 1.40},
    "CPLX": {"Very Low": 0.70, "Low": 0.85, "Nominal": 1.00, "High": 1.15, "Very High": 1.30},
    "ACAP": {"Very Low": 1.46, "Low": 1.19, "Nominal": 1.00, "High": 0.86, "Very High": 0.71},
    "PCAP": {"Very Low": 1.42, "Low": 1.17, "Nominal": 1.00, "High": 0.86, "Very High": 0.70},
    "AEXP": {"Very Low": 1.29, "Low": 1.13, "Nominal": 1.00, "High": 0.91, "Very High": 0.82},
    "TOOL": {"Very Low": 1.24, "Low": 1.10, "Nominal": 1.00, "High": 0.91, "Very High": 0.82}
}

COCOMO_PARAMS = {
    'organic': {'a': 2.4, 'b': 1.05, 'c': 2.5, 'd': 0.38},
    'semi-detached': {'a': 3.0, 'b': 1.12, 'c': 2.5, 'd': 0.35},
    'embedded': {'a': 3.6, 'b': 1.20, 'c': 2.5, 'd': 0.32}
}

def estimate_cocomo(loc: float, mode: str, cost_drivers: Dict[str, str], cost_per_pm: float) -> Dict[str, float]:
    if mode not in COCOMO_PARAMS:
        raise ValueError(f"Invalid mode '{mode}'")

    eaf = calculate_eaf(cost_drivers)
    params = COCOMO_PARAMS[mode]
    effort = params['a'] * (loc ** params['b']) * eaf
    time = params['c'] * (effort ** params['d'])
    people = effort / time
    total_cost = effort * cost_per_pm

    return {
        "eaf": round(eaf, 3),
        "effort_pm": round(effort, 2),
        "development_time_months": round(time, 2),
        "team_size": round(people, 2),
        "total_cost": round(total_cost, 2)
    }

def calculate_eaf(cost_drivers: Dict[str, str]) -> float:
    eaf = 1.0
    for key, rating in cost_drivers.items():
        multiplier = EAF_TABLE.get(key, {}).get(rating, 1.0)
        eaf *= multiplier
    return eaf

def calculate_expert_judgment(estimates: list) -> float:
    """
    计算专家判断的平均值。
    estimates: 专家估算值列表
    """
    if not estimates:
        raise ValueError("Estimate list cannot be empty")
    # 过滤掉非数字值，确保都是浮点数
    valid_estimates = [float(e) for e in estimates if isinstance(e, (int, float))]
    if not valid_estimates:
        raise ValueError("No valid numerical estimates provided.")
    return round(sum(valid_estimates) / len(valid_estimates), 2)


def calculate_delphi_method(rounds: List[List[float]]) -> Dict[str, float]:
    """
    Delphi 方法计算。
    rounds: 多轮专家估算值，每轮是一个列表
    """
    if not rounds or not all(round for round in rounds):
        raise ValueError("Delphi rounds cannot be empty or contain empty rounds.")

    final_estimates = []
    for r in rounds:
        valid_r = [float(e) for e in r if isinstance(e, (int, float))]
        if valid_r:
            final_estimates.extend(valid_r) # 将所有轮次的有效估算值收集起来

    if not final_estimates:
        raise ValueError("No valid estimates found across all Delphi rounds.")

    # 计算最终平均值
    final_average = sum(final_estimates) / len(final_estimates)

    # 计算最终标准差
    if len(final_estimates) > 1:
        std_dev = math.sqrt(sum((x - final_average) ** 2 for x in final_estimates) / (len(final_estimates) - 1))
    else:
        std_dev = 0.0 # 只有一个数据点时标准差为0

    return {
        'final_estimate': round(final_average, 2),
        'std_deviation': round(std_dev, 2),
        'rounds_count': len(rounds) # 报告轮次数量
    }

def calculate_regression_model(inputs: list[tuple[float, float]]) -> dict:
    """
    :param inputs: 输入数据为 [(x1, y1), (x2, y2), ...]
    :return: 回归系数和预测函数
    """
    import statistics

    if len(inputs) < 2:
        raise ValueError("At least two data points are required for regression.")

    xs, ys = zip(*inputs)
    mean_x, mean_y = statistics.mean(xs), statistics.mean(ys)

    # 计算回归系数 b 和截距 a
    b = sum((x - mean_x) * (y - mean_y) for x, y in inputs) / sum((x - mean_x) ** 2 for x in xs)
    a = mean_y - b * mean_x

    def predict(x: float) -> float:
        return round(a + b * x, 2)

    return {
        "intercept_a": round(a, 4),
        "slope_b": round(b, 4),
        "predict_function": predict,
        "sample_count": len(inputs)
    }
