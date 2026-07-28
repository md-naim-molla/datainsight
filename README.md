# DataAuditKit

Automatic Data Quality and EDA Toolkit for Python.

## Features

- **Overview** — rows, columns, memory usage, column type detection (Numeric, Categorical, Boolean, DateTime, Text, HighCardinality)
- **Missing value analysis** — per-column counts/percentages, row-level completeness, nullity correlation patterns
- **Duplicate detection** — exact duplicate row count
- **Numeric statistics** — mean, std, min, quartiles, max via `describe()`
- **Categorical statistics** — top-K frequency tables with automatic "(Other)" binning for high-cardinality columns
- **Correlation analysis** — Pearson, Spearman, or Kendall with heatmap visualization
- **Outlier detection** — IQR method (configurable multiplier) and Z-score method (configurable threshold)
- **Target imbalance** — class distribution with imbalance ratio
- **Leakage detection** — feature-target correlation filter identifying potential data leakage
- **Data quality alerts** — 9 built-in rules (high missing, high cardinality, constant columns, duplicates, high correlation, imbalance, leakage, outliers) with severity levels
- **Health score** — 0–100 quality score computed from triggered alerts
- **Automated remediation** — `fix=True` mode drops constant columns and imputes missing values (median/mode)
- **Rich HTML report** — collapsible sections, embedded base64 plots, color-coded alerts, KPI grid
- **JSON export** — machine-readable report output
- **Dataset comparison** — side-by-side diff of two datasets (row/column changes, alerts, health scores)
- **CLI** — profile and compare commands for CSV/Parquet
- **Database connectors** — `from_sql()` and `from_parquet()` classmethods

## Quickstart

```python
from dataauditkit import ProfileReport

profile = ProfileReport(df, target="Outcome")
profile.to_html("report.html")
```

## Class API

```python
from dataauditkit import ProfileReport, ReportConfig

config = ReportConfig(
    correlation_method="spearman",
    outlier_method="zscore",
    iqr_multiplier=2.0,
    fix_mode=True,
)
profile = ProfileReport(df, target="Outcome", config=config)
profile.compute()                 # run all analysis
profile.to_html("report.html")    # rich HTML report
profile.to_json("report.json")    # machine-readable JSON
profile.to_dict()                 # Python dict (excludes plot data)
profile.cleaned_df                # auto-fixed DataFrame (if fix_mode=True)
```

## Legacy API

```python
from dataauditkit import report

result = report(df, target="Outcome", output=True)
# Returns dict, also writes report.html
```

## CLI Usage

```bash
# Profile a CSV
dataauditkit profile data.csv --target outcome -o report.html --fix

# Compare two datasets
dataauditkit compare data_v1.csv data_v2.csv -o comparison.html
```

## Custom Quality Rules

```python
from dataauditkit import DataQualityRule, evaluate_rules

my_rule = DataQualityRule(
    name="low_row_count",
    description="Dataset has fewer than 100 rows",
    severity="danger",
    condition=lambda r: r["summary"]["rows"] < 100,
)
alerts = evaluate_rules([my_rule], results)
```

## Installation

```bash
pip install dataauditkit
```

Requires Python >= 3.8, pandas, numpy, matplotlib, jinja2.

License: MIT
