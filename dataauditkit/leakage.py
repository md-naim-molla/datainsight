def detect_leakage(df, target, threshold=0.95):
    corr = df.corr(numeric_only=True)

    suspicious = {}

    if target in corr.columns:
        target_corr = corr[target]
        for col, val in target_corr.items():
            if abs(val) > threshold and col != target:
                suspicious[col] = round(val, 3)

    return suspicious