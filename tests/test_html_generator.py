import os
import pandas as pd
from dataauditkit.html_generator import create_html


def test_create_html_basic():
    summary = {"rows": 10, "columns": 3, "memory_mb": 0.01, "duplicates": 0}
    missing = {"missing_count": {"A": 1}, "missing_percent": {"A": 10.0}}
    duplicates = {"duplicates": 0}
    statistics = {"A": {"mean": 5.0, "std": 2.0, "min": 1.0, "max": 9.0}}
    correlation = {"A": {"A": 1.0}}
    outliers = {"A": 0}

    if os.path.exists("report.html"):
        os.remove("report.html")

    create_html(summary, missing, duplicates, statistics, correlation, outliers)

    assert os.path.exists("report.html")
    with open("report.html") as f:
        content = f.read()
    assert "DataAuditKit Report" in content
    assert "Overview" in content
    assert "Missing Values" in content
    assert "Duplicate Rows" in content
    assert "Statistics" in content
    assert "Correlation" in content
    assert "Outliers" in content
    os.remove("report.html")


def test_create_html_with_imbalance_and_leakage():
    summary = {"rows": 10, "columns": 3, "memory_mb": 0.01, "duplicates": 0}
    missing = {"missing_count": {}, "missing_percent": {}}
    duplicates = {"duplicates": 0}
    statistics = {}
    correlation = {}
    outliers = {}
    imbalance = {"class_counts": {0: 7, 1: 3}, "imbalance_ratio": 0.429}
    leakage = {"feature_x": 0.98}

    if os.path.exists("report.html"):
        os.remove("report.html")

    create_html(summary, missing, duplicates, statistics, correlation, outliers,
                imbalance=imbalance, leakage=leakage)

    assert os.path.exists("report.html")
    with open("report.html") as f:
        content = f.read()
    assert "Target Imbalance" in content
    assert "Leakage Detection" in content
    assert "0.429" in content
    assert "0.98" in content
    os.remove("report.html")
