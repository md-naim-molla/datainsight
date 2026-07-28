import pandas as pd
from dataauditkit.missing_patterns import missing_patterns


def test_no_missing():
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    result = missing_patterns(df)
    assert result["rows_complete"] == 3
    assert result["rows_with_any_null"] == 0
    assert result["rows_with_all_null"] == 0
    assert result["pct_complete"] == 100.0


def test_some_missing():
    df = pd.DataFrame({"A": [1, None, 3], "B": [None, 2, 3]})
    result = missing_patterns(df)
    assert result["rows_complete"] == 1
    assert result["rows_with_any_null"] == 2
    assert result["rows_with_all_null"] == 0


def test_all_null_rows():
    df = pd.DataFrame({"A": [None, None, 1], "B": [None, None, 2]})
    result = missing_patterns(df)
    assert result["rows_with_all_null"] == 2
    assert result["rows_complete"] == 1


def test_empty_dataframe():
    df = pd.DataFrame()
    result = missing_patterns(df)
    assert result["rows_complete"] == 0
    assert result["pct_complete"] == 0.0


def test_nullity_correlation():
    df = pd.DataFrame({"A": [1, None, None, 4], "B": [None, 2, None, 4]})
    result = missing_patterns(df)
    assert "nullity_correlation" in result
    assert isinstance(result["nullity_correlation"], dict)
