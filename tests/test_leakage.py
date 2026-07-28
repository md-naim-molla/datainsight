import pandas as pd
import pytest
from dataauditkit.leakage import detect_leakage


def test_no_leakage():
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "target": [0, 0, 1, 1, 0]})
    result = detect_leakage(df, "target")
    assert result == {}


def test_leakage_present():
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "target": [1, 2, 3, 4, 5]})
    result = detect_leakage(df, "target")
    assert "A" in result
    assert abs(result["A"]) > 0.95


def test_leakage_target_not_numeric():
    df = pd.DataFrame({"A": [1, 2, 3], "target": ["x", "y", "z"]})
    result = detect_leakage(df, "target")
    assert result == {}


def test_leakage_excludes_self():
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "target": [1, 2, 3, 4, 5]})
    result = detect_leakage(df, "target")
    assert "target" not in result


def test_leakage_empty_dataframe():
    df = pd.DataFrame()
    result = detect_leakage(df, "target")
    assert result == {}
