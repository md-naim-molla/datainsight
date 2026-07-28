import pandas as pd
from dataauditkit.statistics import numeric_statistics


def test_numeric_statistics_basic():
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [10.0, 20.0, 30.0, 40.0, 50.0]})
    result = numeric_statistics(df)
    assert "A" in result
    assert "B" in result
    assert result["A"]["mean"] == 3.0
    assert result["A"]["min"] == 1.0
    assert result["A"]["max"] == 5.0
    assert result["A"]["50%"] == 3.0


def test_numeric_statistics_no_numeric():
    df = pd.DataFrame({"A": ["x", "y", "z"]})
    result = numeric_statistics(df)
    assert result == {}


def test_numeric_statistics_mixed():
    df = pd.DataFrame({"num": [1, 2, 3], "cat": ["a", "b", "c"]})
    result = numeric_statistics(df)
    assert "num" in result
    assert "cat" not in result


def test_numeric_statistics_single_column():
    df = pd.DataFrame({"A": [10.5]})
    result = numeric_statistics(df)
    assert result["A"]["mean"] == 10.5
    assert result["A"]["count"] == 1.0


def test_numeric_statistics_empty_dataframe():
    df = pd.DataFrame()
    result = numeric_statistics(df)
    assert result == {}
