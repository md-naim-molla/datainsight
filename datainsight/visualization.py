import matplotlib.pyplot as plt

def missing_plot(df):

    missing=df.isnull().sum()

    missing.plot.bar()

    plt.show()