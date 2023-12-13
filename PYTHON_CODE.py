import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from scipy.stats import gmean, variation, skew, kurtosis


def read_df(fname, countries, years):
    """
    Function to read the csv file and return 2 dataframes, one with years
    as columns and the other with countries as columns. Takes the filename as
    the argument.
    """
    # read file into a dataframe
    df0 = pd.read_csv(fname, on_bad_lines='skip', skiprows=4, index_col=0)
    # some cleaning
    df0.drop(columns=["Country Code"], axis=1, inplace=True)
    df1 = df0.loc[countries, years]
    # some dataframe methods
    df1 = df1.sort_index().rename_axis("Years", axis=1).fillna(0)
    # transpose
    df2 = df1.T

    return df1, df2


def stats_df(df):
    """
    Function to do some basic statistics on the dataframes.
    Takes the dataframe with countries as columns as the argument.
    """
    # exploring the dataset
    print("The summary statistics of the dataframe are: \n", df.describe())
    # some basic stats with scipy and dataframe methods
    print(
        "Weighted geometric means of each country are ", gmean(df, axis=0),
        "\n Coefficient of variation of each country are ",
        variation(df, axis=0),
        "\n Maximum values for each country in these years are ",
        df.max(axis=0),
        "\n Minimum values for each country in these years are ",
        df.min(axis=0),
        "\n Skewness is ", skew(df),
        "\n Kurtosis is ", kurtosis(df))

    return


def plot_df(df, knd, title, color):
    """
    Function to plot the dataframes using the dataframe.plot method.

    Arguments:
    The dataframe to be plotted.
    The kind of plot required.
    The title of the figure.
    The color scheme for the plot.

    """
    # using conditional statements for different kinds for better customization
    if knd == "line":
        ax = df.plot(kind=knd, figsize=(7, 5), rot=20, color=color)
        ax.legend(loc='best', fontsize=10)
        ax.set_title(title, fontweight='bold', fontsize='x-large',
                     fontname="Times New Roman")
        ax.set_xlabel("Years", fontweight='bold')
        ax.grid(axis='x', alpha=.85, linewidth=.75)
        plt.savefig(title+".png", dpi=600)
        plt.show()
    else:
        ax = df.plot(kind=knd, figsize=(6.5, 5), rot=20, color=color)
        ax.legend(loc='best', fontsize=10)
        ax.set_title(title, fontweight='bold', fontsize='x-large',
                     fontname="Times New Roman")
        plt.savefig(title+".png", dpi=600, bbox_inches='tight')
        plt.show()

    return


def makeheatmap(filename, country, indicators, c):
    """
    Function to plot the heatmap of a country's indicators. Parameters:
    The name of the csv file containing data of all indicators of
    all countries as a string(should end in .csv).
    The country of which we're plotting the heatmap.
    The list of indicators we're considering for the heat map.
    The color scheme.
    """
    # making the dataframe with which the
    # correlation matrix is to be calculated
    df0 = pd.read_csv(filename, skiprows=4)
    df0.drop(columns=["Country Code", "Indicator Code"], inplace=True)
    # setting multi-index to easily select the country
    df0.set_index(["Country Name", "Indicator Name"], inplace=True)
    df1 = df0.loc[country].fillna(0).T
    # slicing the dataframe to have only the years with nonzero data
    df = df1.loc["1970":"2015", indicators]
    df.rename(columns={
        "Nitrous oxide emissions (thousand metric tons of CO2 equivalent)":
            "N20 Emissions",
        "Energy use (kg of oil equivalent per capita)":
            "Energy Use",
        "Agricultural land (% of land area)":
            "Agricultural land \n(% of land area)",
        "Methane emissions (kt of CO2 equivalent)":
            "Methane emissions \n(kt of CO2 equivalent)",
        "Total greenhouse gas emissions (kt of CO2 equivalent)":
            "Total greenhouse emissions \n(kt of CO2 equivalent)",
        "Arable land (% of land area)":
            "Arable land \n(% of land area)",
        "Forest area (% of land area)":
            "Forest area \n(% of land area)"
    }, inplace=True)
    # plotting the heatmap
    plt.figure(figsize=(6, 4))
    sns.heatmap(df.corr(), cmap=c, annot=True)
    plt.xticks(rotation=90)
    # setting a title and saving the figure
    plt.title(country, fontweight='bold', fontsize='x-large',
              fontname="Times New Roman")
    plt.savefig(country+"'s Heatmap"+".png", dpi=450,
                bbox_inches='tight')
    plt.show()

    return


def calculate_skewness(df):
    """
    Function to calculate skewness of a dataframe.
    """
    return skew(df)


def calculate_kurtosis(df):
    """
    Function to calculate kurtosis of a dataframe.
    """
    return kurtosis(df)


# choosing the countries and years for the dataframes
cntrs = ["Japan", "Russian Federation", "China", "United Kingdom",
         "Brazil", "India", "United States", "Canada"]
yrs = ["1990", "1995", "2000", "2005", "2010", "2015"]

# creating the dataframes using the function
a, b = read_df("API_EN.ATM.CO2E.KT_DS2_en_csv_v2_6224818.csv", cntrs, yrs)
df_co2emissions_1, df_co2emissions_2 = a, b
c, d = read_df("API_EN.ATM.NOXE.KT.CE_DS2_en_csv_v2_6226692.csv", cntrs, yrs)
df_n20emissions_1, df_n20emissions_2 = c, d
e, f = read_df("API_AG.LND.ARBL.ZS_DS2_en_csv_v2_5995308.csv", cntrs, yrs)
df_arableland_1, df_arableland_2 = e, f
g, h = read_df("API_AG.LND.AGRI.ZS_DS2_en_csv_v2_5995314.csv", cntrs, yrs)
df_agricultularland_1, df_agriculturalland_2 = g, h
i, j = read_df("API_AG.LND.FRST.ZS_DS2_en_csv_v2_5994693.csv", cntrs, yrs)
df_forestarea_1, df_forestarea_2 = i, j
k, l = read_df("API_EN.ATM.METH.KT.CE_DS2_en_csv_v2_6232520.csv", cntrs, yrs)
df_methaneemission_1, df_methaneemission_2 = k, l

# creating some cool colormaps for the bar plots
c1 = cm.viridis(np.linspace(.1, .9, 6)[::-1])
c2 = cm.inferno(np.linspace(.2, .9, 6)[::-1])
# some distinctive colors for the line plots
c3 = ['black', 'maroon', 'goldenrod', 'green',
      'teal', 'navy', 'hotpink', 'red']
c4 = ['b', 'g', 'r', 'k', 'm', 'y', 'c', 'brown']

# plotting dataframes with the function
plot_df(df_co2emissions_1, 'bar', 'Carbon Dioxide emissions(kt)', c2)
plot_df(df_n20emissions_1, 'bar',
        'Nitrous Oxide emissions(thousand metric tons of CO2 equivalent)', c1)
plot_df(df_agriculturalland_2, 'line', 'Agricultural land(% of land area)', c3)

# suppressing scientific notation to use the statistical tools
pd.set_option('display.float_format', lambda x: f'{x:,.2f}')

# doing the basic statistics with the function
stats_df(df_co2emissions_2)
stats_df(df_n20emissions_2)

"""
Coefficient of variation was calculated instead of standard deviation because
we would be looking at different datasets of similar type (Carbon dioxide and
Nitrous oxide emissions). This would help us in finding out which countries
had the most relative increase in emissions in that 25 year time period.
"""

# choosing the indicators to make heatmaps
indicators = [
    "Arable land (% of land area)",
    "Forest area (% of land area)",
    "Agricultural land (% of land area)",
    "Nitrous oxide emissions (thousand metric tons of CO2 equivalent)",
    "CO2 emissions (kt)",
    "Total greenhouse gas emissions (kt of CO2 equivalent)",
    "Methane emissions (kt of CO2 equivalent)"
]

# creating some heatmaps to compare indicators of
# countries, explore its correlations (or lack of)
makeheatmap("API_19_DS2_en_csv_v2_6183479.csv", "India", indicators, cm.winter)
makeheatmap("API_19_DS2_en_csv_v2_6183479.csv", "China", indicators, cm.cool)
makeheatmap("API_19_DS2_en_csv_v2_6183479.csv", "Brazil", indicators, cm.bone)
