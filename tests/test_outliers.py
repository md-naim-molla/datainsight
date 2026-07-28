import pandas as pd

from dataauditkit.outliers import detect_outliers


def test_outliers():

    df=pd.DataFrame({

        "A":[1,2,3,4,100]

    })

    result=detect_outliers(df)

    assert result["A"]==1