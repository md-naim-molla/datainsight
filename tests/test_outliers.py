import pandas as pd
from dataauditkit.outliers import detect_outliers


def test_outlier_present():
    df = pd.DataFrame({"A": [1, 2, 3, 4, 100]})
    result = detect_outliers(df)
    assert result["A"] == 1


def test_no_outliers():
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5]})
    result = detect_outliers(df)
    assert result["A"] == 0


def test_outliers_multiple_columns():
    df = pd.DataFrame({"A": [1, 2, 3, 4, 100], "B": [10, 20, 30, 40, 500]})
    result = detect_outliers(df)
    assert result["A"] == 1
    assert result["B"] == 1


def test_non_numeric_columns_skipped():
    df = pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]})
    result = detect_outliers(df)
    assert "A" in result
    assert "B" not in result


def test_constant_column_no_outliers():
    df = pd.DataFrame({"A": [5, 5, 5, 5, 5]})
    result = detect_outliers(df)
    assert result["A"] == 0


def test_empty_dataframe():
    df = pd.DataFrame()
    result = detect_outliers(df)
    assert result == {}


def test_zscore_outliers():
    df = pd.DataFrame({"A": [10, 10, 10, 10, 1000]})
    result = detect_outliers(df, method="zscore", zscore_threshold=1.5)
    assert result["A"] == 1


def test_zscore_no_outliers():
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5]})
    result = detect_outliers(df, method="zscore", zscore_threshold=3.0)
    assert result["A"] == 0


def test_zscore_constant_column():
    df = pd.DataFrame({"A": [5, 5, 5, 5, 5]})
    result = detect_outliers(df, method="zscore")
    assert result["A"] == 0
