import pandas as pd
import numpy as np


def detect_outliers(df, iqr_multiplier=1.5, method="iqr", zscore_threshold=3.0):
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        return {}

    if method == "iqr":
        return _iqr_outliers(numeric, iqr_multiplier)
    elif method == "zscore":
        return _zscore_outliers(numeric, zscore_threshold)
    return {}


def _iqr_outliers(numeric, iqr_multiplier):
    results = {}
    for col in numeric.columns:
        q1 = numeric[col].quantile(0.25)
        q3 = numeric[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - iqr_multiplier * iqr
        upper = q3 + iqr_multiplier * iqr
        count = ((numeric[col] < lower) | (numeric[col] > upper)).sum()
        results[col] = int(count)
    return results


def _zscore_outliers(numeric, threshold):
    results = {}
    for col in numeric.columns:
        mean = numeric[col].mean()
        std = numeric[col].std()
        if std == 0 or pd.isna(std):
            results[col] = 0
            continue
        zscores = (numeric[col] - mean) / std
        count = (zscores.abs() > threshold).sum()
        results[col] = int(count)
    return results
