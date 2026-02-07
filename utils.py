

def test_risk_level_ranges():
    assert risk_level(0.1) == "niskie"
    assert risk_level(0.3) == "umiarkowane"
    assert risk_level(0.5) == "podwyższone"
    assert risk_level(0.8) == "wysokie"
