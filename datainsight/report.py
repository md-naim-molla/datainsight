from .summary import dataset_summary
from .missing import missing_report
from .duplicates import duplicate_report
from .statistics import numeric_statistics
from .correlation import correlation_analysis
from .outliers import detect_outliers
from .imbalance import class_imbalance
from .leakage import detect_leakage
from .html_generator import create_html


def report(
        df,
        target=None,
        output=False
):

    result={}

    result["summary"]=dataset_summary(df)

    result["missing"]=missing_report(df)

    result["duplicates"]=duplicate_report(df)

    result["statistics"]=numeric_statistics(df)

    result["correlation"]=correlation_analysis(df)

    result["outliers"]=detect_outliers(df)

    if target:

        result["imbalance"]=(
            class_imbalance(
                df,
                target
            )
        )

        result["leakage"]=(
            detect_leakage(
                df,
                target
            )
        )

    if output:

        create_html(
            result["summary"],
            result["missing"],
            result["outliers"]
        )

    return result