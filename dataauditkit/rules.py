class DataQualityRule:
    def __init__(self, name, description, condition, severity="warning"):
        self.name = name
        self.description = description
        self.condition = condition
        self.severity = severity

    def evaluate(self, results):
        try:
            triggered = self.condition(results)
            return {
                "name": self.name,
                "description": self.description,
                "severity": self.severity,
                "triggered": triggered,
            }
        except Exception:
            return {
                "name": self.name,
                "description": self.description,
                "severity": self.severity,
                "triggered": False,
                "error": True,
            }


def build_default_rules(config=None):
    return [
        DataQualityRule(
            name="high_missing",
            description="Columns with >50% missing values",
            severity="danger",
            condition=lambda r: any(
                pct > 50 for pct in r.get("missing", {}).get("missing_percent", {}).values()
            ),
        ),
        DataQualityRule(
            name="high_cardinality",
            description="Columns with unusually high cardinality",
            severity="warning",
            condition=lambda r: any(
                t == "HighCardinality"
                for t in r.get("summary", {}).get("column_types", {}).values()
            ),
        ),
        DataQualityRule(
            name="constant_columns",
            description="Columns with zero variance (constant values)",
            severity="info",
            condition=lambda r: any(
                stats.get("std", -1) == 0 or stats.get("std") != stats.get("std")
                for stats in r.get("statistics", {}).values()
            ),
        ),
        DataQualityRule(
            name="duplicate_rows",
            description="Dataset contains duplicate rows",
            severity="warning",
            condition=lambda r: r.get("duplicates", {}).get("duplicates", 0) > 0,
        ),
        DataQualityRule(
            name="missing_values",
            description="Dataset has missing values",
            severity="info",
            condition=lambda r: any(
                c > 0 for c in r.get("missing", {}).get("missing_count", {}).values()
            ),
        ),
        DataQualityRule(
            name="high_correlation",
            description="Features with near-perfect correlation (|r| > 0.95)",
            severity="warning",
            condition=lambda r: _has_high_correlation(r),
        ),
        DataQualityRule(
            name="target_imbalance",
            description="Target column has class imbalance",
            severity="warning",
            condition=lambda r: r.get("imbalance", {}).get("imbalance_ratio", 1) < 0.5,
        ),
        DataQualityRule(
            name="data_leakage",
            description="Potential data leakage detected",
            severity="danger",
            condition=lambda r: len(r.get("leakage", {})) > 0,
        ),
        DataQualityRule(
            name="outliers_detected",
            description="Outliers found in numerical columns",
            severity="info",
            condition=lambda r: any(c > 0 for c in r.get("outliers", {}).values()),
        ),
    ]


def _has_high_correlation(results):
    corr = results.get("correlation", {})
    for col1, row in corr.items():
        for col2, val in row.items():
            if col1 != col2 and abs(val) > 0.95:
                return True
    return False


def evaluate_rules(rules, results):
    return [rule.evaluate(results) for rule in rules]


def compute_health_score(alerts):
    if not alerts:
        return 100
    triggered = [a for a in alerts if a["triggered"]]
    if not triggered:
        return 100

    deductions = {"info": 5, "warning": 15, "danger": 30}
    penalty = sum(deductions.get(a["severity"], 10) for a in triggered)
    return max(0, min(100, 100 - penalty))
