from jinja2 import Environment
from jinja2 import FileSystemLoader


def create_html(
        summary,
        missing,
        outliers
):

    env=Environment(
        loader=FileSystemLoader(
            "templates"
        )
    )

    template=env.get_template(
        "report_template.html"
    )

    html=template.render(

        summary=summary,
        missing=missing,
        outliers=outliers

    )

    with open(
            "report.html",
            "w",
            encoding="utf-8"
    ) as f:

        f.write(html)