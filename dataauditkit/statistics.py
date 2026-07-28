def numeric_statistics(df):

    numeric=df.select_dtypes(
        include="number"
    )

    return numeric.describe().to_dict()


def categorical_statistics(df):

    categorical=df.select_dtypes(
        exclude="number"
    )

    return categorical.describe().to_dict()