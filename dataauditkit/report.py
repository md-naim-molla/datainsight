from .summary import dataset_summary
from .missing import missing_report
from .duplicates import duplicate_report
from .statistics import numeric_statistics
from .correlation import correlation_analysis
from .outliers import detect_outliers
from .imbalance import class_imbalance
from .leakage import detect_leakage
from .html_generator import create_html
from .visualization import missing_plot, correlation_plot


def report(df, target=None, output=False):
    result = {}

    result["summary"] = dataset_summary(df)
    result["missing"] = missing_report(df)
    result["duplicates"] = duplicate_report(df)
    result["statistics"] = numeric_statistics(df)
    result["correlation"] = correlation_analysis(df)
    result["outliers"] = detect_outliers(df)

    if target:
        result["imbalance"] = class_imbalance(df, target)
        result["leakage"] = detect_leakage(df, target)

    if output:
        missing_plot(df)
        correlation_plot(df)
        create_html(
            summary=result["summary"],
            missing=result["missing"],
            duplicates=result["duplicates"],
            statistics=result["statistics"],
            correlation=result["correlation"],
            outliers=result["outliers"],
            imbalance=result.get("imbalance"),
            leakage=result.get("leakage"),
        )

    return result
