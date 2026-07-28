def numeric_statistics(df):
    numeric = df.select_dtypes(include="number")
    if numeric.empty or numeric.columns.size == 0:
        return {}
    return numeric.describe().to_dict()