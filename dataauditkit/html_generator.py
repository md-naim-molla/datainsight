import os
from importlib import resources
from jinja2 import Template


def create_html(
    summary,
    missing,
    duplicates,
    statistics,
    correlation,
    outliers,
    imbalance=None,
    leakage=None,
    missing_plot=None,
    correlation_plot=None,
    alerts=None,
    missing_patterns=None,
    categorical_statistics=None,
    fix_log=None,
    output_path=".",
    filename="report.html",
):
    template_content = resources.read_text(
        "dataauditkit", "report_template.html"
    )
    template = Template(template_content)

    html = template.render(
        summary=summary,
        missing=missing,
        duplicates=duplicates,
        statistics=statistics,
        correlation=correlation,
        outliers=outliers,
        imbalance=imbalance,
        leakage=leakage,
        missing_plot=missing_plot,
        correlation_plot=correlation_plot,
        alerts=alerts or [],
        missing_patterns=missing_patterns,
        categorical_statistics=categorical_statistics,
        fix_log=fix_log,
    )

    filepath = os.path.join(output_path, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
