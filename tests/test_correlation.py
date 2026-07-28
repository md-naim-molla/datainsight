import pandas as pd
import pytest
from dataauditkit.correlation import correlation_analysis


def test_correlation_positive():
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [2, 4, 6, 8, 10]})
    result = correlation_analysis(df)
    assert "A" in result
    assert "B" in result
    assert result["A"]["B"] == pytest.approx(1.0, rel=0.01)


def test_correlation_negative():
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [10, 8, 6, 4, 2]})
    result = correlation_analysis(df)
    assert result["A"]["B"] == pytest.approx(-1.0, rel=0.01)


def test_correlation_no_numeric():
    df = pd.DataFrame({"A": ["x", "y", "z"]})
    result = correlation_analysis(df)
    assert result == {}


def test_correlation_single_column():
    df = pd.DataFrame({"A": [1, 2, 3]})
    result = correlation_analysis(df)
    assert "A" in result
    assert result["A"]["A"] == pytest.approx(1.0, rel=0.01)


def test_correlation_no_correlation():
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [5, 5, 5, 5, 5]})
    result = correlation_analysis(df)
    assert result["A"]["B"] != result["A"]["B"]


def test_correlation_empty_dataframe():
    df = pd.DataFrame()
    result = correlation_analysis(df)
    assert result == {}
