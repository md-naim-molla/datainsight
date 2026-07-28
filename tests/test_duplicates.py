import pandas as pd
from dataauditkit.duplicates import duplicate_report


def test_duplicates():

    df=pd.DataFrame({

        "A":[1,1,2]

    })

    result=duplicate_report(df)

    assert result["duplicates"]==1