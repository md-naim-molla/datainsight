import pandas as pd
from datainsight.missing import missing_report


def test_missing():

    df = pd.DataFrame({

        "A":[1,None,3]

    })

    result = missing_report(df)

    assert result["missing_count"]["A"]==1