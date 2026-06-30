import matplotlib.pyplot as plt


def missing_plot(df):

    missing=df.isnull().sum()

    missing.plot.bar()

    plt.savefig(
        "missing_values.png"
    )

    plt.close()


def correlation_plot(df):

    corr=df.corr(
        numeric_only=True
    )

    plt.imshow(corr)

    plt.colorbar()

    plt.xticks(
        range(len(corr.columns)),
        corr.columns,
        rotation=90
    )

    plt.yticks(
        range(len(corr.columns)),
        corr.columns
    )

    plt.savefig(
        "correlation.png"
    )

    plt.close()