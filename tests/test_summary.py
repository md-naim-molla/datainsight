import pandas as pd
from dataauditkit.summary import dataset_summary


def test_summary_basic():
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4.0, 5.0, 6.0]})
    result = dataset_summary(df)
    assert result["rows"] == 3
    assert result["columns"] == 2
    assert isinstance(result["memory_mb"], float)
    assert result["memory_mb"] >= 0


def test_summary_empty():
    df = pd.DataFrame()
    result = dataset_summary(df)
    assert result["rows"] == 0
    assert result["columns"] == 0


def test_summary_with_duplicates():
    df = pd.DataFrame({"A": [1, 1, 2]})
    result = dataset_summary(df)
    assert result["duplicates"] == 1


def test_summary_no_duplicates():
    df = pd.DataFrame({"A": [1, 2, 3]})
    result = dataset_summary(df)
    assert result["duplicates"] == 0


def test_summary_single_row():
    df = pd.DataFrame({"A": [1], "B": ["x"]})
    result = dataset_summary(df)
    assert result["rows"] == 1
    assert result["columns"] == 2


def test_summary_large_dataset():
    df = pd.DataFrame({"A": range(10000), "B": range(10000, 20000)})
    result = dataset_summary(df)
    assert result["rows"] == 10000
    assert result["columns"] == 2
