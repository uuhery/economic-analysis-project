from typing import List
import numpy_financial as npf

def calculate_npv(cash_flows: List[float], discount_rate: float) -> float:
    return round(sum(cf / ((1 + discount_rate) ** t) for t, cf in enumerate(cash_flows)), 2)

def calculate_roi(gain: float, cost: float) -> float:
    if cost == 0:
        raise ValueError("Cost cannot be zero")
    return round((gain - cost) / cost * 100, 2)  # 百分比

def calculate_irr(cash_flows: List[float]) -> float:
    irr = npf.irr(cash_flows)
    if irr is None:
        raise ValueError("IRR could not be calculated.")
    return round(irr * 100, 2)

def calculate_payback(cash_flows: List[float]) -> float:
    cumulative = 0
    for i, flow in enumerate(cash_flows):
        cumulative += flow
        if cumulative >= 0:
            return i  # 回本时间点（单位：期数）
    return -1  # 没有回本

def track_budget(data: List[dict]) -> List[dict]:
    result = []
    for item in data:
        phase = item.get("phase")
        budget = item.get("budgeted_amount", 0)
        actual = item.get("actual_amount", 0)
        difference = actual - budget
        result.append({
            "phase": phase,
            "budgeted_amount": budget,
            "actual_amount": actual,
            "difference": round(difference, 2)
        })
    return result

def analyze_variance(data: List[dict]) -> List[dict]:
    result = []
    for item in data:
        phase = item.get("phase")
        budget = item.get("budgeted_amount", 0)
        actual = item.get("actual_amount", 0)
        difference = round(actual - budget, 2)
        percent_variance = round((difference / budget * 100) if budget else 0, 2)

        if percent_variance > 10:
            analysis = "Overspent"
        elif percent_variance < -10:
            analysis = "Underspent"
        else:
            analysis = "Within range"

        result.append({
            "phase": phase,
            "budgeted_amount": budget,
            "actual_amount": actual,
            "difference": difference,
            "percent_variance": percent_variance,
            "analysis": analysis
        })
    return result

def forecast_next_phase(data: List[dict]) -> dict:
    if len(data) < 2:
        raise ValueError("Need at least 2 phases for forecasting.")

    b1, b2 = data[-2]["budgeted_amount"], data[-1]["budgeted_amount"]
    a1, a2 = data[-2]["actual_amount"], data[-1]["actual_amount"]

    budget_growth = ((b2 - b1) / b1) if b1 else 0
    actual_growth = ((a2 - a1) / a1) if a1 else 0

    forecast_budget = data[-1]["budgeted_amount"] * (1 + budget_growth)
    forecast_actual = data[-1]["actual_amount"] * (1 + actual_growth)

    return {
        "forecast_phase": f"Forecast-{len(data)+1}",
        "forecast_budgeted": round(forecast_budget, 2),
        "forecast_actual": round(forecast_actual, 2),
        "budget_growth_rate": round(budget_growth * 100, 2),
        "actual_growth_rate": round(actual_growth * 100, 2)
    }
