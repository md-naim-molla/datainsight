def dataset_summary(df):

    result={}

    result["rows"]=df.shape[0]

    result["columns"]=df.shape[1]

    result["memory_mb"]=round(
        df.memory_usage().sum()/1024**2,
        2
    )

    result["duplicates"]=df.duplicated().sum()

    return result