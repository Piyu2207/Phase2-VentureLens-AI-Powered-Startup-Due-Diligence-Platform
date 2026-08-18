from backend.dspy_engine.metrics import bad_output_example,validate_dict
def test_bad_output_rejected(): assert validate_dict(bad_output_example()) is False
def test_valid_output_accepted():
    x={"verdict":"INVEST","confidence":91,"financial_risk":"LOW","market_risk":"MEDIUM","network_strength":"HIGH",
       "reasoning":"Strong financial performance and network evidence support the verdict."}
    assert validate_dict(x) is True
