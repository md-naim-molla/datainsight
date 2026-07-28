import os
import sqlite3
import pandas as pd
import pytest
from dataauditkit.profile import ProfileReport
from dataauditkit.config import ReportConfig


@pytest.fixture
def df():
    return pd.DataFrame({
        "num": [1, 2, 3, 4, 5],
        "cat": ["a", "b", "c", "d", "e"],
        "const": [1, 1, 1, 1, 1],
    })


def test_profile_includes_alerts(df):
    profile = ProfileReport(df)
    results = profile.compute()
    assert "alerts" in results
    assert len(results["alerts"]) > 0


def test_profile_includes_missing_patterns(df):
    profile = ProfileReport(df)
    results = profile.compute()
    assert "missing_patterns" in results


def test_profile_includes_categorical_stats(df):
    profile = ProfileReport(df)
    results = profile.compute()
    assert "categorical_statistics" in results


def test_profile_fix_mode_drops_constants(df):
    config = ReportConfig(fix_mode=True)
    profile = ProfileReport(df, config=config)
    results = profile.compute()
    assert "fix_log" in results
    assert "const" in results["fix_log"]["dropped_columns"]


def test_profile_fix_mode_imputes_missing():
    df = pd.DataFrame({"A": [1, None, 3], "B": [None, "x", "y"]})
    config = ReportConfig(fix_mode=True)
    profile = ProfileReport(df, config=config)
    results = profile.compute()
    assert profile.cleaned_df is not None
    assert profile.cleaned_df["A"].isna().sum() == 0
    assert "A" in results["fix_log"]["imputed_columns"] or "B" in results["fix_log"]["imputed_columns"]


def test_from_sql(df):
    conn = sqlite3.connect(":memory:")
    df.to_sql("test", conn, index=False)
    profile = ProfileReport.from_sql("SELECT * FROM test", conn)
    conn.close()
    assert isinstance(profile, ProfileReport)
    results = profile.compute()
    assert results["summary"]["rows"] == 5


def test_from_parquet(tmp_path, df):
    pytest.importorskip("pyarrow")
    path = tmp_path / "test.parquet"
    df.to_parquet(path)
    profile = ProfileReport.from_parquet(str(path))
    assert isinstance(profile, ProfileReport)
    results = profile.compute()
    assert results["summary"]["rows"] == 5


def test_profile_to_html_includes_alerts(df):
    profile = ProfileReport(df)
    profile.to_html("/tmp/test_phase3.html")
    with open("/tmp/test_phase3.html") as f:
        content = f.read()
    assert "Data Quality Alerts" in content
    os.remove("/tmp/test_phase3.html")


def test_profile_categorical_statistics_in_html(df):
    profile = ProfileReport(df)
    profile.to_html("/tmp/test_cat.html")
    with open("/tmp/test_cat.html") as f:
        content = f.read()
    assert "Categorical Statistics" in content
    os.remove("/tmp/test_cat.html")
