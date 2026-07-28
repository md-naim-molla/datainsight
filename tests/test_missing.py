import pandas as pd
import pytest
from dataauditkit.missing import missing_report


def test_missing_some():
    df = pd.DataFrame({"A": [1, None, 3]})
    result = missing_report(df)
    assert result["missing_count"]["A"] == 1
    assert result["missing_percent"]["A"] == pytest.approx(33.33, rel=0.01)


def test_missing_none():
    df = pd.DataFrame({"A": [1, 2, 3]})
    result = missing_report(df)
    assert result["missing_count"]["A"] == 0
    assert result["missing_percent"]["A"] == 0.0


def test_missing_all():
    df = pd.DataFrame({"A": [None, None, None]})
    result = missing_report(df)
    assert result["missing_count"]["A"] == 3
    assert result["missing_percent"]["A"] == 100.0


def test_missing_multiple_columns():
    df = pd.DataFrame({"A": [1, None, None], "B": [None, 2, 3]})
    result = missing_report(df)
    assert result["missing_count"]["A"] == 2
    assert result["missing_count"]["B"] == 1
    assert result["missing_percent"]["A"] == pytest.approx(66.67, rel=0.01)
    assert result["missing_percent"]["B"] == pytest.approx(33.33, rel=0.01)


def test_missing_empty_dataframe():
    df = pd.DataFrame()
    result = missing_report(df)
    assert result["missing_count"] == {}
    assert result["missing_percent"] == {}
