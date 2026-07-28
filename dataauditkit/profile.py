import json
import os
import warnings

from .config import ReportConfig
from .types import detect_column_types, summarize_types
from .summary import dataset_summary
from .missing import missing_report
from .duplicates import duplicate_report
from .statistics import numeric_statistics, categorical_statistics
from .correlation import correlation_analysis
from .outliers import detect_outliers
from .imbalance import class_imbalance
from .leakage import detect_leakage
from .missing_patterns import missing_patterns
from .rules import build_default_rules, evaluate_rules, compute_health_score
from .html_generator import create_html
from .visualization import missing_plot_base64, correlation_plot_base64


class ProfileReport:
    def __init__(self, df, target=None, config=None):
        self._df = df
        self._target = target
        self._config = config or ReportConfig()
        self._results = None
        self._cleaned_df = None

    @property
    def config(self):
        return self._config

    def compute(self):
        config = self._config
        df = self._df
        target = self._target
        results = {}

        if config.fix_mode:
            df, fix_log = self._apply_fixes(df)
            results["fix_log"] = fix_log
            self._cleaned_df = df

        column_types = detect_column_types(df, config.cardinality_threshold)
        results["summary"] = dataset_summary(df)
        results["summary"]["column_types"] = column_types
        results["summary"]["type_summary"] = summarize_types(column_types)

        results["missing"] = missing_report(df)
        results["duplicates"] = duplicate_report(df)

        results["statistics"] = numeric_statistics(df)

        if config.compute_categorical_stats:
            results["categorical_statistics"] = categorical_statistics(
                df, config.cardinality_threshold, config.max_categories
            )

        if config.compute_correlation:
            if len(df.columns) > config.max_correlation_columns:
                warnings.warn(
                    f"Correlation skipped: {len(df.columns)} columns exceeds "
                    f"max_correlation_columns ({config.max_correlation_columns}). "
                    f"Set compute_correlation=False or increase max_correlation_columns."
                )
                results["correlation"] = {}
            else:
                results["correlation"] = correlation_analysis(df, method=config.correlation_method)
        else:
            results["correlation"] = {}

        if config.detect_outliers:
            results["outliers"] = detect_outliers(
                df,
                iqr_multiplier=config.iqr_multiplier,
                method=config.outlier_method,
                zscore_threshold=config.zscore_threshold,
            )
        else:
            results["outliers"] = {}

        if config.compute_missing_patterns:
            results["missing_patterns"] = missing_patterns(df)

        if target:
            results["imbalance"] = class_imbalance(df, target)
            results["leakage"] = detect_leakage(df, target, threshold=config.leakage_threshold)

        if config.generate_plots:
            results["missing_plot"] = missing_plot_base64(df)
            results["correlation_plot"] = correlation_plot_base64(df)

        results["alerts"] = evaluate_rules(build_default_rules(config), results)
        results["health_score"] = compute_health_score(results["alerts"])

        self._results = results
        return results

    def _apply_fixes(self, df):
        fix_log = {"dropped_columns": [], "imputed_columns": []}

        for col in df.columns:
            if df[col].nunique(dropna=False) == 1:
                fix_log["dropped_columns"].append(col)
                df = df.drop(columns=[col])

        for col in df.select_dtypes(include="number").columns:
            if col in df.columns and df[col].isna().any():
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                fix_log["imputed_columns"].append(col)

        for col in df.select_dtypes(exclude="number").columns:
            if col in df.columns and df[col].isna().any():
                mode_val = df[col].mode()
                if not mode_val.empty:
                    df[col] = df[col].fillna(mode_val[0])
                    fix_log["imputed_columns"].append(col)

        return df, fix_log

    @property
    def results(self):
        if self._results is None:
            self.compute()
        return self._results

    @property
    def cleaned_df(self):
        if self._cleaned_df is None and self._config.fix_mode:
            self.compute()
        return self._cleaned_df

    def to_dict(self):
        result = {}
        for key, val in self.results.items():
            if key.endswith("_plot"):
                continue
            result[key] = val
        return result

    def to_html(self, filepath="report.html"):
        config = self._config
        create_html(
            summary=self.results["summary"],
            missing=self.results["missing"],
            duplicates=self.results["duplicates"],
            statistics=self.results["statistics"],
            correlation=self.results.get("correlation", {}),
            outliers=self.results.get("outliers", {}),
            imbalance=self.results.get("imbalance"),
            leakage=self.results.get("leakage"),
            missing_plot=self.results.get("missing_plot"),
            correlation_plot=self.results.get("correlation_plot"),
            alerts=self.results.get("alerts", []),
            missing_patterns=self.results.get("missing_patterns"),
            categorical_statistics=self.results.get("categorical_statistics"),
            fix_log=self.results.get("fix_log"),
            output_path=config.output_path,
            filename=filepath,
        )

    def to_json(self, filepath="report.json"):
        path = os.path.join(self._config.output_path, filepath)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, default=str)
        return path

    @classmethod
    def from_sql(cls, query, connection, target=None, config=None, **kwargs):
        import pandas as pd
        df = pd.read_sql(query, connection, **kwargs)
        return cls(df, target=target, config=config)

    @classmethod
    def from_parquet(cls, path, target=None, config=None, **kwargs):
        import pandas as pd
        df = pd.read_parquet(path, **kwargs)
        return cls(df, target=target, config=config)
