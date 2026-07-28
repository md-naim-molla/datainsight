import pandas as pd
from dataauditkit.compare import compare_datasets


def test_compare_same_datasets():
    df1 = pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]})
    df2 = pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]})
    html = compare_datasets(df1, df2)
    assert "DataAuditKit Comparison" in html
    assert "Row Count" in html
    assert "Columns" in html


def test_compare_different_rows():
    df1 = pd.DataFrame({"A": [1, 2, 3]})
    df2 = pd.DataFrame({"A": [1, 2]})
    html = compare_datasets(df1, df2)
    assert "3" in html
    assert "2" in html


def test_compare_different_columns():
    df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    df2 = pd.DataFrame({"A": [1, 2], "C": [5, 6]})
    html = compare_datasets(df1, df2)
    assert "Column Changes" in html


def test_compare_shows_health_scores():
    df1 = pd.DataFrame({"A": [1, 2, 3]})
    df2 = pd.DataFrame({"A": [1, 2, 3]})
    html = compare_datasets(df1, df2)
    assert "Health Score" in html


def test_compare_shows_alerts():
    df1 = pd.DataFrame({"A": [1, 2, None]})
    df2 = pd.DataFrame({"A": [1, 2, 3]})
    html = compare_datasets(df1, df2)
    assert "Alerts" in html
