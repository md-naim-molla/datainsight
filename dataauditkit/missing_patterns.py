import pandas as pd
import numpy as np


def missing_patterns(df):
    total_rows = len(df)

    rows_with_any_null = int(df.isna().any(axis=1).sum())
    rows_with_all_null = int(df.isna().all(axis=1).sum())
    rows_complete = total_rows - rows_with_any_null

    nullity_corr = _nullity_correlation(df)

    return {
        "rows_with_any_null": rows_with_any_null,
        "rows_with_all_null": rows_with_all_null,
        "rows_complete": rows_complete,
        "pct_complete": round(rows_complete / total_rows * 100, 2) if total_rows else 0.0,
        "nullity_correlation": nullity_corr,
    }


def _nullity_correlation(df):
    missing_df = df.isna().astype(int)
    numeric = missing_df.select_dtypes(include="number")
    if numeric.shape[1] < 2:
        return {}
    corr = numeric.corr()
    result = {}
    for col1 in corr.columns:
        row = {}
        for col2 in corr.columns:
            if col1 != col2:
                val = corr.loc[col1, col2]
                if not pd.isna(val):
                    row[col2] = round(val, 3)
        if row:
            result[col1] = row
    return result
