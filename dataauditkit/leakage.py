def detect_leakage(
        df,
        target
):

    corr=df.corr(
        numeric_only=True
    )

    suspicious={}

    if target in corr.columns:

        target_corr=corr[target]

        for col,val in target_corr.items():

            if abs(val)>0.95 and col!=target:

                suspicious[col]=round(
                    val,
                    3
                )

    return suspicious