def calculate_cocomo(loc: float, mode: str = 'organic') -> float:
    params = {
        'organic': (2.4, 1.05),
        'semi-detached': (3.0, 1.12),
        'embedded': (3.6, 1.20)
    }
    if mode not in params:
        raise ValueError(f"Invalid mode '{mode}'")

    a, b = params[mode]
    effort = a * (loc ** b)
    return round(effort, 2)

def calculate_fp(inputs: dict, avg_effort_per_fp: float = 20.0) -> dict:
    weights = {
        'external_inputs': 3,
        'external_outputs': 4,
        'external_inquiries': 3,
        'internal_files': 7,
        'external_interfaces': 5
    }
    total_fp = sum(inputs.get(k, 0) * weights[k] for k in weights)
    return {
        "function_points": total_fp,
        "estimated_effort_hours": round(total_fp * avg_effort_per_fp, 2)
    }

def calculate_expert_judgment(estimates: list) -> float:
    if not estimates:
        raise ValueError("Estimate list cannot be empty")
    return round(sum(estimates) / len(estimates), 2)

def calculate_delphi_method(rounds: list[list[float]]) -> dict:
    """
    :param rounds: 每一轮专家评估值列表的列表（如 [[80, 100, 90], [85, 95, 88]]）
    :return: 最后一轮的均值和标准差
    """
    import statistics

    if not rounds or not all(isinstance(r, list) and r for r in rounds):
        raise ValueError("Each round must be a non-empty list of estimates")

    final_round = rounds[-1]
    avg = round(statistics.mean(final_round), 2)
    std_dev = round(statistics.stdev(final_round), 2) if len(final_round) > 1 else 0.0

    return {
        "final_estimate": avg,
        "std_deviation": std_dev,
        "rounds_count": len(rounds)
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
