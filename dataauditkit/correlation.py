def correlation_analysis(df, method="pearson"):
    numeric = df.select_dtypes(include="number")
    if numeric.empty or numeric.columns.size == 0:
        return {}
    return numeric.corr(method=method).to_dict()