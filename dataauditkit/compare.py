import pandas as pd


def compare_datasets(df1, df2, name1="Dataset 1", name2="Dataset 2"):
    from .profile import ProfileReport
    profile1 = ProfileReport(df1)
    profile2 = ProfileReport(df2)
    r1 = profile1.compute()
    r2 = profile2.compute()

    sections = []

    # Row diff
    sections.append(_section("Row Count", [
        _row(name1, str(r1["summary"]["rows"])),
        _row(name2, str(r2["summary"]["rows"])),
        _row("Difference", str(r1["summary"]["rows"] - r2["summary"]["rows"])),
    ]))

    # Column diff
    cols1 = set(df1.columns)
    cols2 = set(df2.columns)
    sections.append(_section("Columns", [
        _row("Columns in both", str(len(cols1 & cols2))),
        _row(f"Only in {name1}", str(len(cols1 - cols2))),
        _row(f"Only in {name2}", str(len(cols2 - cols1))),
    ]))

    # Missing values
    sections.append(_section("Missing Values", [
        _row(f"{name1} total missing", str(sum(r1["missing"]["missing_count"].values()))),
        _row(f"{name2} total missing", str(sum(r2["missing"]["missing_count"].values()))),
        _row(f"{name1} duplicates", str(r1["duplicates"]["duplicates"])),
        _row(f"{name2} duplicates", str(r2["duplicates"]["duplicates"])),
    ]))

    # Health scores
    h1 = r1.get("health_score", "N/A")
    h2 = r2.get("health_score", "N/A")
    sections.append(_section("Health Score", [
        _row(f"{name1} score", str(h1)),
        _row(f"{name2} score", str(h2)),
    ]))

    # Alerts
    a1 = [a for a in r1.get("alerts", []) if a["triggered"]]
    a2 = [a for a in r2.get("alerts", []) if a["triggered"]]
    sections.append(_section("Alerts", [
        _row(f"{name1} triggered", str(len(a1))),
        _row(f"{name2} triggered", str(len(a2))),
    ]))

    return _render_comparison_html(sections, name1, name2, r1, r2)


def _section(title, rows):
    return {"title": title, "rows": rows}


def _row(label, value):
    return {"label": label, "value": value}


def _render_comparison_html(sections, name1, name2, r1, r2):
    rows1 = r1["summary"]["rows"]
    rows2 = r2["summary"]["rows"]
    html = f"""<!DOCTYPE html>
<html>
<head><title>DataAuditKit Comparison</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f5f6fa;color:#2c3e50;}}
.header{{background:#2c3e50;color:#fff;padding:30px 40px;}}
.header h1{{margin:0;font-size:28px;}}
.container{{max-width:1000px;margin:0 auto;padding:20px;}}
.card{{background:#fff;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.08);margin-bottom:20px;overflow:hidden;}}
.card-header{{padding:16px 24px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;user-select:none;}}
.card-header h2{{margin:0;font-size:18px;color:#2c3e50;}}
.card-body{{padding:16px 24px 24px;border-top:1px solid #ecf0f1;}}
.card-body.hidden{{display:none;}}
table{{border-collapse:collapse;width:100%;margin:8px 0;}}
th,td{{border:1px solid #e0e0e0;padding:10px 12px;text-align:left;font-size:14px;}}
th{{background:#f8f9fa;font-weight:600;color:#34495e;}}
tr:hover{{background:#fafafa;}}
.tag{{display:inline-block;padding:2px 8px;border-radius:12px;font-size:12px;font-weight:600;margin:2px;}}
.tag-added{{background:#d4edda;color:#155724;}}
.tag-removed{{background:#f8d7da;color:#721c24;}}
.tag-common{{background:#d1ecf1;color:#0c5460;}}
</style>
</head>
<body>
<div class="header">
<h1>DataAuditKit Comparison</h1>
<p>{name1} ({rows1} rows) vs {name2} ({rows2} rows)</p>
</div>
<div class="container">
"""

    cols1 = set(r1.get("summary", {}).get("column_types", {}).keys())
    cols2 = set(r2.get("summary", {}).get("column_types", {}).keys())
    common = cols1 & cols2
    only1 = cols1 - cols2
    only2 = cols2 - cols1

    html += """<div class="card">
<div class="card-header"><h2>Column Changes</h2></div>
<div class="card-body">"""
    if only1:
        html += '<div style="margin:8px 0;">'
        for c in sorted(only1):
            html += f'<span class="tag tag-removed">{c}</span> '
        html += f"<p style='margin-top:4px;font-size:13px;color:#721c24;'>Removed in {name2}</p></div>"
    if only2:
        html += '<div style="margin:8px 0;">'
        for c in sorted(only2):
            html += f'<span class="tag tag-added">{c}</span> '
        html += f"<p style='margin-top:4px;font-size:13px;color:#155724;'>Added in {name2}</p></div>"
    if common:
        html += '<div style="margin:8px 0;">'
        for c in sorted(common):
            html += f'<span class="tag tag-common">{c}</span> '
        html += f"<p style='margin-top:4px;font-size:13px;color:#0c5460;'>Common ({len(common)})</p></div>"
    html += "</div></div>"

    for section in sections:
        html += f"""<div class="card">
<div class="card-header" onclick="toggle(this)"><h2>{section['title']}</h2><span class="toggle">&#9660;</span></div>
<div class="card-body">
<table><tr><th>Metric</th><th>Value</th></tr>"""
        for row in section["rows"]:
            html += f"<tr><td>{row['label']}</td><td>{row['value']}</td></tr>"
        html += "</table></div></div>"

    html += """</div>
<script>
function toggle(el){
var body=el.nextElementSibling;
var arrow=el.querySelector('.toggle');
body.classList.toggle('hidden');
arrow.classList.toggle('open');
}
</script>
</body>
</html>"""
    return html
