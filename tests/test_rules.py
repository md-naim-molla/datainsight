import pandas as pd
from dataauditkit.rules import DataQualityRule, build_default_rules, evaluate_rules


def test_rule_basic():
    rule = DataQualityRule(
        name="test",
        description="Always triggered",
        condition=lambda r: True,
        severity="warning",
    )
    result = rule.evaluate({})
    assert result["name"] == "test"
    assert result["triggered"] is True
    assert result["severity"] == "warning"


def test_rule_not_triggered():
    rule = DataQualityRule(
        name="test",
        description="Never triggered",
        condition=lambda r: False,
    )
    result = rule.evaluate({})
    assert result["triggered"] is False


def test_rule_error_handling():
    rule = DataQualityRule(
        name="broken",
        description="Throws exception",
        condition=lambda r: 1 / 0,
    )
    result = rule.evaluate({})
    assert result["triggered"] is False
    assert result["error"] is True


def test_build_default_rules():
    rules = build_default_rules()
    assert len(rules) > 0
    assert any(r.name == "missing_values" for r in rules)
    assert any(r.name == "duplicate_rows" for r in rules)
    assert any(r.name == "outliers_detected" for r in rules)


def test_evaluate_rules():
    rules = [
        DataQualityRule("pass", "passes", lambda r: True),
        DataQualityRule("fail", "fails", lambda r: False),
    ]
    results = evaluate_rules(rules, {})
    assert len(results) == 2
    assert results[0]["triggered"] is True
    assert results[1]["triggered"] is False


def test_high_missing_rule():
    rules = build_default_rules()
    high_missing = [r for r in rules if r.name == "high_missing"][0]
    result = high_missing.evaluate({"missing": {"missing_percent": {"A": 60}}})
    assert result["triggered"] is True
    result2 = high_missing.evaluate({"missing": {"missing_percent": {"A": 10}}})
    assert result2["triggered"] is False
