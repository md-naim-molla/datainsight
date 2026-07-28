def detect_outliers(df):

    results={}

    numeric=df.select_dtypes(
        include="number"
    )

    for col in numeric.columns:

        q1=numeric[col].quantile(.25)

        q3=numeric[col].quantile(.75)

        iqr=q3-q1

        lower=q1-1.5*iqr

        upper=q3+1.5*iqr

        count=((numeric[col]<lower)|
               (numeric[col]>upper)
               ).sum()

        results[col]=int(count)

    return results