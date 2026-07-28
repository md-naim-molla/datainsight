import pandas as pd
from dataauditkit.statistics import categorical_statistics


def test_categorical_basic():
    df = pd.DataFrame({"A": ["a", "b", "c", "a", "b"]})
    result = categorical_statistics(df)
    assert "A" in result
    assert result["A"]["count"] == 5
    assert result["A"]["nunique"] == 3
    assert result["A"]["missing"] == 0


def test_categorical_with_missing():
    df = pd.DataFrame({"A": ["a", None, "b", None, "c"]})
    result = categorical_statistics(df)
    assert result["A"]["missing"] == 2
    assert result["A"]["missing_pct"] == 40.0
    assert result["A"]["count"] == 3


def test_categorical_no_categorical_columns():
    df = pd.DataFrame({"A": [1, 2, 3]})
    result = categorical_statistics(df)
    assert result == {}


def test_categorical_top_values():
    df = pd.DataFrame({"A": ["x", "x", "y", "z"]})
    result = categorical_statistics(df, max_categories=20)
    assert result["A"]["top_values"]["x"] == 2
    assert result["A"]["top_values"]["y"] == 1
    assert result["A"]["top_values"]["z"] == 1


def test_categorical_top_values_with_other():
    values = [f"v{i}" for i in range(30)]
    df = pd.DataFrame({"A": values * 2})
    result = categorical_statistics(df, max_categories=5)
    assert "(Other)" in result["A"]["top_values"]


def test_categorical_empty_dataframe():
    df = pd.DataFrame()
    result = categorical_statistics(df)
    assert result == {}
