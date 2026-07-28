import pandas as pd


def numeric_statistics(df):
    numeric = df.select_dtypes(include="number")
    if numeric.empty or numeric.columns.size == 0:
        return {}
    return numeric.describe().to_dict()


def categorical_statistics(df, cardinality_threshold=50, max_categories=20):
    categorical = df.select_dtypes(exclude="number")
    if categorical.empty or categorical.columns.size == 0:
        return {}

    result = {}
    for col in categorical.columns:
        counts = categorical[col].value_counts()
        total = len(categorical[col].dropna())
        nunique = len(counts)

        stats = {
            "count": int(categorical[col].notna().sum()),
            "nunique": nunique,
            "missing": int(categorical[col].isna().sum()),
            "missing_pct": round(categorical[col].isna().mean() * 100, 2),
        }

        if total > 0:
            if nunique <= max_categories:
                top_k = counts.head(max_categories).to_dict()
            else:
                top_k = counts.head(max_categories - 1).to_dict()
                other_count = counts.iloc[max_categories - 1:].sum()
                top_k["(Other)"] = int(other_count)

            stats["top_values"] = {
                str(k): int(v) for k, v in top_k.items()
            }

        result[col] = stats

    return result
