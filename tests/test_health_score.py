import pandas as pd
from dataauditkit.rules import compute_health_score


def test_perfect_score():
    alerts = [{"name": "a", "severity": "info", "triggered": False}]
    assert compute_health_score(alerts) == 100


def test_empty_alerts():
    assert compute_health_score([]) == 100


def test_info_deduction():
    alerts = [{"name": "a", "severity": "info", "triggered": True}]
    assert compute_health_score(alerts) == 95


def test_warning_deduction():
    alerts = [{"name": "a", "severity": "warning", "triggered": True}]
    assert compute_health_score(alerts) == 85


def test_danger_deduction():
    alerts = [{"name": "a", "severity": "danger", "triggered": True}]
    assert compute_health_score(alerts) == 70


def test_multiple_deductions():
    alerts = [
        {"name": "a", "severity": "info", "triggered": True},
        {"name": "b", "severity": "warning", "triggered": True},
        {"name": "c", "severity": "danger", "triggered": True},
    ]
    assert compute_health_score(alerts) == 50


def test_clamped_minimum():
    alerts = [
        {"name": "a", "severity": "danger", "triggered": True},
        {"name": "b", "severity": "danger", "triggered": True},
        {"name": "c", "severity": "danger", "triggered": True},
        {"name": "d", "severity": "danger", "triggered": True},
    ]
    assert compute_health_score(alerts) == 0


def test_health_score_in_profile():
    df = pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]})
    from dataauditkit import ProfileReport
    profile = ProfileReport(df)
    results = profile.compute()
    assert "health_score" in results
    assert 0 <= results["health_score"] <= 100
