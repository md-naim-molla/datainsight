import io
import base64
import matplotlib.pyplot as plt


def _missing_data(df):
    return df.isnull().sum()


def _correlation_data(df):
    return df.corr(numeric_only=True)


def missing_plot_base64(df):
    missing = _missing_data(df)
    if missing.empty:
        plt.close()
        return ""
    fig, ax = plt.subplots()
    missing.plot.bar(ax=ax)
    ax.set_title("Missing Values by Column")
    ax.set_ylabel("Count")
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def correlation_plot_base64(df):
    corr = _correlation_data(df)
    if corr.empty:
        plt.close()
        return ""
    fig, ax = plt.subplots()
    im = ax.imshow(corr, cmap="viridis")
    plt.colorbar(im, ax=ax)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=90)
    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns)
    ax.set_title("Correlation Matrix")
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def missing_plot_save(df, path="missing_values.png"):
    missing = _missing_data(df)
    if missing.empty:
        plt.close()
        return
    fig, ax = plt.subplots()
    missing.plot.bar(ax=ax)
    ax.set_title("Missing Values by Column")
    ax.set_ylabel("Count")
    plt.savefig(path, bbox_inches="tight")
    plt.close()


def correlation_plot_save(df, path="correlation.png"):
    corr = _correlation_data(df)
    if corr.empty:
        plt.close()
        return
    fig, ax = plt.subplots()
    im = ax.imshow(corr, cmap="viridis")
    plt.colorbar(im, ax=ax)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=90)
    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns)
    ax.set_title("Correlation Matrix")
    plt.savefig(path, bbox_inches="tight")
    plt.close()


missing_plot = missing_plot_save
correlation_plot = correlation_plot_save
