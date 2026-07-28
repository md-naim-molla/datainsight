# DataAuditkit

Automatic Data Quality and EDA Toolkit for Python.

Features:

- Dataset overview
- Missing-value analysis
- Duplicate detection
- Numeric statistics
- Categorical statistics
- Correlation analysis
- Outlier detection
- Target imbalance analysis
- Leakage detection
- Visualization
- HTML report generation

Example:

```python
from dataauditkit import report

result = report(
    df,
    target="Outcome"
)

print(result)