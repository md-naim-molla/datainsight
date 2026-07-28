import pandas as pd
from dataauditkit.duplicates import duplicate_report


def test_duplicates_some():
    df = pd.DataFrame({"A": [1, 1, 2]})
    result = duplicate_report(df)
    assert result["duplicates"] == 1


def test_duplicates_none():
    df = pd.DataFrame({"A": [1, 2, 3]})
    result = duplicate_report(df)
    assert result["duplicates"] == 0


def test_duplicates_all():
    df = pd.DataFrame({"A": [1, 1, 1]})
    result = duplicate_report(df)
    assert result["duplicates"] == 2


def test_duplicates_multiple_columns():
    df = pd.DataFrame({"A": [1, 1, 2], "B": [4, 4, 5]})
    result = duplicate_report(df)
    assert result["duplicates"] == 1


def test_duplicates_empty():
    df = pd.DataFrame()
    result = duplicate_report(df)
    assert result["duplicates"] == 0


def test_duplicates_single_row():
    df = pd.DataFrame({"A": [1]})
    result = duplicate_report(df)
    assert result["duplicates"] == 0


def test_duplicates_returns_int():
    df = pd.DataFrame({"A": [1, 1, 2]})
    result = duplicate_report(df)
    assert isinstance(result["duplicates"], int)
