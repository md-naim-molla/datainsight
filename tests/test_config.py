import pytest
from dataauditkit.config import ReportConfig


def test_default_config():
    config = ReportConfig()
    assert config.iqr_multiplier == 1.5
    assert config.correlation_method == "pearson"
    assert config.leakage_threshold == 0.95
    assert config.cardinality_threshold == 50
    assert config.generate_plots is True


def test_custom_config():
    config = ReportConfig(
        iqr_multiplier=2.0,
        correlation_method="spearman",
        leakage_threshold=0.9,
        cardinality_threshold=100,
        generate_plots=False,
    )
    assert config.iqr_multiplier == 2.0
    assert config.correlation_method == "spearman"
    assert config.leakage_threshold == 0.9
    assert config.cardinality_threshold == 100
    assert config.generate_plots is False


def test_invalid_correlation_method():
    with pytest.raises(ValueError, match="correlation_method"):
        ReportConfig(correlation_method="invalid")


def test_invalid_iqr_multiplier():
    with pytest.raises(ValueError, match="iqr_multiplier"):
        ReportConfig(iqr_multiplier=0)


def test_invalid_leakage_threshold_low():
    with pytest.raises(ValueError, match="leakage_threshold"):
        ReportConfig(leakage_threshold=0)


def test_invalid_leakage_threshold_high():
    with pytest.raises(ValueError, match="leakage_threshold"):
        ReportConfig(leakage_threshold=1.0)
