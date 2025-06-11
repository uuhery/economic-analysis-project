import math
import statistics
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

def calculate_expert_judgment(experts: list[dict]) -> dict:
    """
    计算加权平均、标准差、极值、平均置信度。
    """
    if not experts:
        raise ValueError("Expert list cannot be empty")

    weights = []
    estimates = []

    for e in experts:
        est = e["estimate"]
        conf = e["confidence"]
        if not (0 <= conf <= 1):
            raise ValueError(f"Confidence must be between 0 and 1. Got: {conf}")
        estimates.append(est)
        weights.append(conf)

    total_weight = sum(weights)
    if total_weight == 0:
        raise ValueError("Total confidence weight cannot be zero.")

    weighted_sum = sum(est * w for est, w in zip(estimates, weights))
    weighted_avg = weighted_sum / total_weight

    # 标准差（不加权）
    mean = sum(estimates) / len(estimates)
    variance = sum((x - mean) ** 2 for x in estimates) / len(estimates)
    std_dev = math.sqrt(variance)

    return {
        "weighted_average": round(weighted_avg, 2),
        "std_deviation": round(std_dev, 2),
        "min": round(min(estimates), 2),
        "max": round(max(estimates), 2),
        "avg_confidence": round(sum(weights) / len(weights), 2)
    }

def calculate_delphi_method(rounds: List[List[float]], threshold: float) -> Dict:
    """
    Delphi 方法计算，包括每轮均值、标准差、是否收敛。
    """
    if not rounds or not all(round for round in rounds):
        raise ValueError("Delphi rounds cannot be empty or contain empty rounds.")

    history = []
    converged = False

    for i, r in enumerate(rounds):
        valid = [float(e) for e in r if isinstance(e, (int, float))]
        if not valid:
            continue
        mean = sum(valid) / len(valid)
        std = math.sqrt(sum((x - mean) ** 2 for x in valid) / len(valid)) if len(valid) > 1 else 0.0

        history.append({
            "round": i + 1,
            "mean": round(mean, 2),
            "std": round(std, 2)
        })

        if std < threshold:
            converged = True
            break

    final_round = history[-1] if history else {"mean": 0, "std": 0}

    return {
        "final_estimate": final_round["mean"],
        "std_deviation": final_round["std"],
        "rounds_count": len(history),
        "convergence": converged,
        "estimate_history": history
    }

def calculate_regression_model(inputs: List[List[float]], predict_x: float) -> Dict:
    if len(inputs) < 2:
        raise ValueError("At least two data points are required for regression.")

    xs, ys = zip(*inputs)
    mean_x, mean_y = statistics.mean(xs), statistics.mean(ys)

    # 回归系数 b 和截距 a
    b = sum((x - mean_x) * (y - mean_y) for x, y in inputs) / sum((x - mean_x) ** 2 for x in xs)
    a = mean_y - b * mean_x

    # 拟合优度 R²
    ss_tot = sum((y - mean_y) ** 2 for y in ys)
    ss_res = sum((y - (a + b * x)) ** 2 for x, y in inputs)
    r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else 0

    return {
        "intercept_a": round(a, 4),
        "slope_b": round(b, 4),
        "predict_y": round(a + b * predict_x, 2),
        "sample_count": len(inputs),
        "r_squared": round(r_squared, 4)
    }

