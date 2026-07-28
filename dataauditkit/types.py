import pandas as pd


def detect_column_types(df, cardinality_threshold=50):
    types = {}
    for col in df.columns:
        dtype = df[col].dtype
        if pd.api.types.is_bool_dtype(dtype):
            types[col] = "Boolean"
        elif pd.api.types.is_numeric_dtype(dtype):
            types[col] = "Numeric"
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            types[col] = "DateTime"
        elif pd.api.types.is_string_dtype(dtype) or isinstance(dtype, pd.CategoricalDtype) or pd.api.types.is_object_dtype(dtype):
            nunique = df[col].nunique()
            if nunique == 2:
                types[col] = "Boolean"
            elif nunique <= cardinality_threshold:
                types[col] = "Categorical"
            else:
                avg_len = df[col].astype(str).str.len().mean()
                if avg_len > 50:
                    types[col] = "Text"
                else:
                    types[col] = "HighCardinality"
        else:
            types[col] = "Unknown"
    return types


def summarize_types(types):
    summary = {}
    for t in types.values():
        summary[t] = summary.get(t, 0) + 1
    return summary
