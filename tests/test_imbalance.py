import pandas as pd

from dataauditkit.imbalance import class_imbalance


def test_imbalance():

    df=pd.DataFrame({

        "y":[0,0,0,1]

    })

    result=class_imbalance(
        df,
        "y"
    )

    assert result[
        "imbalance_ratio"
    ]==0.333