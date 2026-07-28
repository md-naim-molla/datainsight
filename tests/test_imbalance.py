import pandas as pd
from dataauditkit.imbalance import class_imbalance


def test_imbalanced():
    df = pd.DataFrame({"y": [0, 0, 0, 1]})
    result = class_imbalance(df, "y")
    assert result["imbalance_ratio"] == 0.333
    assert result["class_counts"] == {0: 3, 1: 1}


def test_balanced():
    df = pd.DataFrame({"y": [0, 0, 1, 1]})
    result = class_imbalance(df, "y")
    assert result["imbalance_ratio"] == 1.0


def test_multiclass():
    df = pd.DataFrame({"y": [0, 0, 0, 1, 1, 2]})
    result = class_imbalance(df, "y")
    assert result["imbalance_ratio"] == 0.333
    assert set(result["class_counts"].keys()) == {0, 1, 2}


def test_single_class():
    df = pd.DataFrame({"y": [0, 0, 0]})
    result = class_imbalance(df, "y")
    assert result["imbalance_ratio"] == 1.0


def test_string_labels():
    df = pd.DataFrame({"y": ["cat", "cat", "dog"]})
    result = class_imbalance(df, "y")
    assert result["imbalance_ratio"] == 0.5


def test_large_imbalance():
    df = pd.DataFrame({"y": [0] * 100 + [1] * 900})
    result = class_imbalance(df, "y")
    assert result["imbalance_ratio"] == 0.111
