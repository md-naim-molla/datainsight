from dataclasses import dataclass


@dataclass
class ReportConfig:
    iqr_multiplier: float = 1.5
    correlation_method: str = "pearson"
    leakage_threshold: float = 0.95
    cardinality_threshold: int = 50
    max_categories: int = 20
    compute_correlation: bool = True
    detect_outliers: bool = True
    generate_plots: bool = True
    output_path: str = "."

    outlier_method: str = "iqr"
    zscore_threshold: float = 3.0
    max_correlation_columns: int = 50
    fix_mode: bool = False
    compute_missing_patterns: bool = True
    compute_categorical_stats: bool = True
    max_unique_display: int = 30

    def __post_init__(self):
        valid_methods = ["pearson", "spearman", "kendall"]
        if self.correlation_method not in valid_methods:
            raise ValueError(
                f"correlation_method must be one of {valid_methods}, "
                f"got '{self.correlation_method}'"
            )
        if self.iqr_multiplier <= 0:
            raise ValueError(
                f"iqr_multiplier must be positive, got {self.iqr_multiplier}"
            )
        if not 0 < self.leakage_threshold < 1:
            raise ValueError(
                f"leakage_threshold must be between 0 and 1, "
                f"got {self.leakage_threshold}"
            )
        valid_outlier = ["iqr", "zscore"]
        if self.outlier_method not in valid_outlier:
            raise ValueError(
                f"outlier_method must be one of {valid_outlier}, "
                f"got '{self.outlier_method}'"
            )
        if self.zscore_threshold <= 0:
            raise ValueError(
                f"zscore_threshold must be positive, got {self.zscore_threshold}"
            )
