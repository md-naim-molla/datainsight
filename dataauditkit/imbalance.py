def class_imbalance(
        df,
        target
):

    counts=df[
        target
    ].value_counts()

    ratio=round(
        counts.min()/counts.max(),
        3
    )

    return {

        "class_counts":
        counts.to_dict(),

        "imbalance_ratio":
        ratio

    }