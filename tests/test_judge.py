import pytest

from backend.dspy_engine.metrics import bad_output_example, validate_dict

def test_bad_output_rejected():
    assert validate_dict(bad_output_example()) is False


def test_valid_output_accepted():
    x = {
        "verdict": "INVEST",
        "confidence": 91,
        "financial_risk": "LOW",
        "market_risk": "MEDIUM",
        "network_strength": "HIGH",
        "reasoning": "Strong financial performance and network evidence support the verdict.",
    }
    assert validate_dict(x) is True


@pytest.mark.parametrize(
    "bad",
    [
        {
            "verdict": "MAYBE",
            "confidence": 70,
            "financial_risk": "LOW",
            "market_risk": "LOW",
            "network_strength": "HIGH",
            "reasoning": "Evidence supports the company.",
        },
        {
            "verdict": "INVEST",
            "confidence": 101,
            "financial_risk": "LOW",
            "market_risk": "LOW",
            "network_strength": "HIGH",
            "reasoning": "Evidence supports the company.",
        },
        {
            "verdict": "INVEST",
            "confidence": 80,
            "financial_risk": "UNKNOWN",
            "market_risk": "LOW",
            "network_strength": "HIGH",
            "reasoning": "Evidence supports the company.",
        },
        {
            "verdict": "INVEST",
            "confidence": 80,
            "financial_risk": "LOW",
            "market_risk": "LOW",
            "network_strength": "HIGH",
            "reasoning": "",
        },
        {
            "verdict": "INVEST",
            "confidence": 80,
            "financial_risk": "LOW",
            "market_risk": "LOW",
            "network_strength": "HIGH",
            "reasoning": "As an AI, I cannot determine the result.",
        },
    ],
)

def test_judge_rejects_realistic_bad_outputs(bad):
    assert validate_dict(bad) is False
