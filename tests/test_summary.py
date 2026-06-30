import pandas as pd

from datainsight.summary import dataset_summary


def test_summary():

    df=pd.DataFrame({

        "A":[1,2,3]

    })

    result=dataset_summary(df)

    assert result["rows"]==3