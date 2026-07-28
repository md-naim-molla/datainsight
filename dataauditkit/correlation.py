def correlation_analysis(df):

    numeric=df.select_dtypes(
        include="number"
    )

    return numeric.corr().to_dict()