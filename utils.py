
def risk_level(p_high: float) -> str:
    if p_high < 0.20:
        return "niskie"
    if p_high < 0.40:
        return "umiarkowane"
    if p_high < 0.60:
        return "podwyższone"
    return "wysokie"
