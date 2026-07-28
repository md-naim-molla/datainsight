import os
import pandas as pd
from dataauditkit.visualization import missing_plot, correlation_plot


def test_missing_plot_creates_file():
    df = pd.DataFrame({"A": [1, None, 3], "B": [None, 2, None]})
    if os.path.exists("missing_values.png"):
        os.remove("missing_values.png")
    missing_plot(df)
    assert os.path.exists("missing_values.png")
    os.remove("missing_values.png")


def test_missing_plot_no_missing():
    df = pd.DataFrame({"A": [1, 2, 3]})
    if os.path.exists("missing_values.png"):
        os.remove("missing_values.png")
    missing_plot(df)
    assert os.path.exists("missing_values.png")
    os.remove("missing_values.png")


def test_correlation_plot_creates_file():
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    if os.path.exists("correlation.png"):
        os.remove("correlation.png")
    correlation_plot(df)
    assert os.path.exists("correlation.png")
    os.remove("correlation.png")


def test_correlation_plot_single_column():
    df = pd.DataFrame({"A": [1, 2, 3]})
    if os.path.exists("correlation.png"):
        os.remove("correlation.png")
    correlation_plot(df)
    assert os.path.exists("correlation.png")
    os.remove("correlation.png")
