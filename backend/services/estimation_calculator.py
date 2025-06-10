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
