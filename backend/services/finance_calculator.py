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