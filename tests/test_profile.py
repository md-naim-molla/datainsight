import os
import json
import pandas as pd
import pytest
from dataauditkit.profile import ProfileReport
from dataauditkit.config import ReportConfig


@pytest.fixture
def df():
    return pd.DataFrame({
        "num": [1, 2, 3, 4, 5],
        "cat": ["a", "b", "c", "d", "e"],
        "target": [0, 0, 1, 1, 0],
    })


def test_profile_compute(df):
    profile = ProfileReport(df)
    results = profile.compute()
    assert "summary" in results
    assert "missing" in results
    assert "statistics" in results
    assert "correlation" in results
    assert "outliers" in results
    assert "missing_plot" in results
    assert "correlation_plot" in results


def test_profile_lazy_compute(df):
    profile = ProfileReport(df)
    assert profile._results is None
    results = profile.results
    assert profile._results is not None


def test_profile_with_target(df):
    profile = ProfileReport(df, target="target")
    results = profile.compute()
    assert "imbalance" in results
    assert "leakage" in results


def test_profile_without_target(df):
    profile = ProfileReport(df)
    results = profile.compute()
    assert "imbalance" not in results
    assert "leakage" not in results


def test_profile_to_dict(df):
    profile = ProfileReport(df, target="target")
    d = profile.to_dict()
    assert "summary" in d
    assert "missing" in d
    assert "missing_plot" not in d
    assert "correlation_plot" not in d


def test_profile_to_html(df):
    profile = ProfileReport(df, target="target")
    profile.to_html("test_report.html")
    assert os.path.exists("test_report.html")
    with open("test_report.html") as f:
        content = f.read()
    assert "DataAuditKit Report" in content
    assert "Overview" in content
    assert "Target Imbalance" in content
    os.remove("test_report.html")


def test_profile_to_json(df):
    profile = ProfileReport(df, target="target")
    path = profile.to_json("test_report.json")
    assert os.path.exists(path)
    with open(path) as f:
        data = json.load(f)
    assert "summary" in data
    assert "statistics" in data
    assert "imbalance" in data
    os.remove("test_report.json")


def test_profile_custom_config(df):
    config = ReportConfig(
        correlation_method="spearman",
        iqr_multiplier=2.0,
        leakage_threshold=0.8,
        compute_correlation=True,
        detect_outliers=True,
        generate_plots=False,
    )
    profile = ProfileReport(df, target="target", config=config)
    results = profile.compute()
    assert "missing_plot" not in results
    assert "correlation_plot" not in results
    assert "correlation" in results
    assert "outliers" in results


def test_profile_disabled_analysis(df):
    config = ReportConfig(
        compute_correlation=False,
        detect_outliers=False,
        generate_plots=False,
    )
    profile = ProfileReport(df, config=config)
    results = profile.compute()
    assert results["correlation"] == {}
    assert results["outliers"] == {}


def test_profile_empty_dataframe():
    df = pd.DataFrame()
    profile = ProfileReport(df)
    results = profile.compute()
    assert results["summary"]["rows"] == 0
    assert results["statistics"] == {}
    assert results["correlation"] == {}
