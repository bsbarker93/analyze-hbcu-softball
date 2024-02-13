#import modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re


#clear trailing periods
def clean_team(df):
    '''
    clean_team generates cleaned up dataframe
    :param df: original dataframe
    :return: dataframe with trailing periods removed'''
    #save team column as list with trailing periods substituted
    df["Team"] = [re.sub(r'\.\.+', '', x) for x in df["Team"]]
    return df

def create_barplot(df, cols, x="variable", y="value", hue=None, palette=None, title=None):
    '''
    create_barplot generates a seaborn barplot with customized features
    :param df: melted dataframe
    :param cols: list of columns of interest
    :param x: column to be plotted on the x axis
    :param y: column to be plotted on the y axis
    :param hue: column to be used as legend
    :param palette: dictionary of teams and their color
    :param title: string plot title
    :return: None
    '''
    fig1 = plt.figure()
    # set plot style
    sns.barplot(data= df.loc[df[x].isin(cols)], x=x, y=y, hue=hue, palette=palette ) 
    # edit plot features
    plt.xticks(rotation=0)
    plt.xlabel("Stats")
    plt.ylabel(y.title())
    plt.title(title)
    plt.show()
    return 

year = 2011
# create dictionary for dataframes based on table type
dict_dfs = {'AVG':'', 'ERA':'', 'C':''}
#loop through dictionary to create dataframes
for k,v in dict_dfs.items():
    filename = f"./hbcu-softball/data/MEAC-{year}-{k}.csv"
    dict_dfs[k] = pd.read_csv(filename)
# store dataframes
df_avg = dict_dfs['AVG']
df_era = dict_dfs['ERA']
df_c = dict_dfs['C']
clean_team(df_avg)

#rivalry charts
rivals = ["Howard", "Hampton"]
# set color palette based on school colors
palette = {rivals[0]: "midnightblue", rivals[1]: "cornflowerblue"}
# isolate rows of interest in new df
data = df_avg.loc[df_avg["Team"].isin(rivals)]
title = f"The Real HU - {year}"
# melt df for easier seaborn plotting
try_data = data.melt(id_vars="Team")
# loop through barplot function using a list of columns of interest
variables = [["AB"], ["AVG", "SLG%", "OB%"], ["G", "H", "2B", "3B", "HR", "R", "RBI"]]
for item in variables:
    create_barplot(try_data, item, "variable", "value", "Team", palette, title)
