def duplicate_report(df):

    return {

        "duplicates":
        int(df.duplicated().sum())

    }