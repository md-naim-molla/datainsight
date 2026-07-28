import argparse
import sys

from .config import ReportConfig
from .profile import ProfileReport


def main():
    parser = argparse.ArgumentParser(
        description="DataAuditKit — Automatic Data Quality and EDA Toolkit"
    )
    sub = parser.add_subparsers(dest="command")

    profile_parser = sub.add_parser("profile", help="Generate a data profile report")
    profile_parser.add_argument("input", help="Path to CSV or Parquet file")
    profile_parser.add_argument("--target", help="Target column name")
    profile_parser.add_argument("--output", "-o", default="report.html", help="Output HTML file path")
    profile_parser.add_argument("--json", action="store_true", help="Also export JSON report")
    profile_parser.add_argument("--correlation", default="pearson", choices=["pearson", "spearman", "kendall"])
    profile_parser.add_argument("--outlier-method", default="iqr", choices=["iqr", "zscore"])
    profile_parser.add_argument("--fix", action="store_true", help="Auto-fix mode")
    profile_parser.add_argument("--max-categories", type=int, default=20, help="Max categories to display")

    compare_parser = sub.add_parser("compare", help="Compare two datasets")
    compare_parser.add_argument("input1", help="Path to first CSV")
    compare_parser.add_argument("input2", help="Path to second CSV")
    compare_parser.add_argument("--output", "-o", default="comparison.html", help="Output HTML file path")

    args = parser.parse_args()

    if args.command == "profile":
        _run_profile(args)
    elif args.command == "compare":
        _run_compare(args)
    else:
        parser.print_help()
        sys.exit(1)


def _load_data(path):
    import pandas as pd
    if path.endswith(".parquet"):
        return pd.read_parquet(path)
    return pd.read_csv(path)


def _run_profile(args):
    config = ReportConfig(
        correlation_method=args.correlation,
        outlier_method=args.outlier_method,
        fix_mode=args.fix,
        max_categories=args.max_categories,
    )
    df = _load_data(args.input)
    profile = ProfileReport(df, target=args.target, config=config)
    profile.to_html(filepath=args.output)

    triggered = [
        a for a in profile.results.get("alerts", []) if a["triggered"]
    ]
    score = profile.results.get("health_score", 100)
    print(f"Report: {args.output}")
    print(f"Health score: {score}/100")
    print(f"Alerts triggered: {len(triggered)}")
    if triggered:
        for a in triggered:
            print(f"  [{a['severity']}] {a['name']}: {a['description']}")

    if args.json:
        json_path = args.output.replace(".html", ".json")
        profile.to_json(filepath=json_path)
        print(f"JSON: {json_path}")


def _run_compare(args):
    from .compare import compare_datasets
    df1 = _load_data(args.input1)
    df2 = _load_data(args.input2)
    html = compare_datasets(df1, df2)
    with open(args.output, "w") as f:
        f.write(html)
    print(f"Comparison report: {args.output}")
