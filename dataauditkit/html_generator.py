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
    )

    with open(
        "report.html",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(html)
