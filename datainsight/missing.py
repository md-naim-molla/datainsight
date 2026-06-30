def missing_report(df):

    missing=df.isnull().sum()

    percent=round(
        (missing/len(df))*100,
        2
    )

    result={

        "missing_count":
        missing.to_dict(),

        "missing_percent":
        percent.to_dict()

    }

    return result