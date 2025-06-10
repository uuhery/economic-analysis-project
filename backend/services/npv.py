def calculate_npv(cash_flows, discount_rate):
    """
    cash_flows: List[float], e.g. [-1000, 300, 400, 500]
    discount_rate: float, e.g. 0.1
    """
    npv = sum(cf / ((1 + discount_rate) ** t) for t, cf in enumerate(cash_flows))
    return round(npv, 2)
