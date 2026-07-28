import os
import pandas as pd
import pytest
from dataauditkit.report import report


@pytest.fixture
def df():
    return pd.DataFrame({
        "num": [1, 2, 3, 4, 5],
        "cat": ["a", "b", "c", "d", "e"],
        "target": [0, 0, 1, 1, 0],
    })


def test_report_returns_dict(df):
    result = report(df)
    assert isinstance(result, dict)


def test_report_all_sections_present(df):
    result = report(df)
    assert "summary" in result
    assert "missing" in result
    assert "duplicates" in result
    assert "statistics" in result
    assert "correlation" in result
    assert "outliers" in result


def test_report_with_target_adds_imbalance_and_leakage(df):
    result = report(df, target="target")
    assert "imbalance" in result
    assert "leakage" in result


def test_report_without_target_omits_imbalance_and_leakage(df):
    result = report(df)
    assert "imbalance" not in result
    assert "leakage" not in result


def test_report_output_generates_html(df):
    result = report(df, target="target", output=True)
    assert os.path.exists("report.html")
    os.remove("report.html")
    assert os.path.exists("missing_values.png")
    os.remove("missing_values.png")
    assert os.path.exists("correlation.png")
    os.remove("correlation.png")


def test_report_no_output_no_files(df):
    result = report(df)
    assert not os.path.exists("report.html")
    assert not os.path.exists("missing_values.png")
    assert not os.path.exists("correlation.png")


def test_report_summary_content(df):
    result = report(df)
    assert result["summary"]["rows"] == 5
    assert result["summary"]["columns"] == 3


def test_report_empty_dataframe():
    df = pd.DataFrame()
    result = report(df)
    assert result["summary"]["rows"] == 0
