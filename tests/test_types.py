import pandas as pd
from dataauditkit.types import detect_column_types, summarize_types


def test_detect_numeric():
    df = pd.DataFrame({"A": [1, 2, 3]})
    types = detect_column_types(df)
    assert types["A"] == "Numeric"


def test_detect_boolean():
    df = pd.DataFrame({"A": [True, False, True]})
    types = detect_column_types(df)
    assert types["A"] == "Boolean"


def test_detect_boolean_from_binary_int():
    df = pd.DataFrame({"A": [0, 1, 0, 1]})
    types = detect_column_types(df)
    assert types["A"] == "Numeric"


def test_detect_categorical():
    df = pd.DataFrame({"A": ["cat", "dog", "bird"]})
    types = detect_column_types(df, cardinality_threshold=50)
    assert types["A"] == "Categorical"


def test_detect_high_cardinality():
    df = pd.DataFrame({"A": [f"val_{i}" for i in range(100)]})
    types = detect_column_types(df, cardinality_threshold=50)
    assert types["A"] == "HighCardinality"


def test_detect_datetime():
    df = pd.DataFrame({"A": pd.to_datetime(["2021-01-01", "2021-01-02", "2021-01-03"])})
    types = detect_column_types(df)
    assert types["A"] == "DateTime"


def test_summarize_types():
    types = {"a": "Numeric", "b": "Numeric", "c": "Categorical"}
    summary = summarize_types(types)
    assert summary == {"Numeric": 2, "Categorical": 1}


def test_empty_dataframe():
    df = pd.DataFrame()
    types = detect_column_types(df)
    assert types == {}
