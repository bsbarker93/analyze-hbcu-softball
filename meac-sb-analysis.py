#import modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from thefuzz import process, fuzz


def clean_team(df):
        ''' 
        clean_team generates cleaned up dataframe
        :param df: original dataframe
        :return: dataframe with trailing periods removed and university shorthand names replaced'''
        #save team column as list with trailing periods substituted
        df['team'] = [re.sub(r'\.\.+', '', x) for x in df['team']]
        #clarify SC in SC State
        df['team'] = [re.sub('SC State', 'South Carolina St', x) for x in df['team']]
        #full names of school saved to variable
        schools = ['Delaware State', 'Coppin State', 'Bethune-Cookman', 'Florida A&M', 
                             'Norfolk State', 'Howard', 'Morgan State', 'Hampton', 'North Carolina A&T',
                             'South Carolina State', 'Maryland Eastern Shore', 'Savannah State',
                             'North Carolina Central', 'Totals']
        #collapse school names according to variable
        #[print(f'{item}  -to-  {process.extractOne(item, schools, scorer=fuzz.token_sort_ratio)[0]}') for item in df["team"].unique()]
        df['team'] = df["team"].apply(lambda x: process.extractOne(x, schools, scorer=fuzz.partial_ratio)[0])
        return df

def combine_years(yr_start, yr_stop, type):
        '''
        combine_years combines the csvs for the indicated years for the specified type of stats
        :param yr_start: number of 4 digits
        df_all = pd.DataFrame()
        for year in range(yr_start, yr_stop):
            #create dataframe for the year's table
            df_yr = pd.read_csv(f"./hbcu-softball/data/MEAC-{year}-{type}.csv")
            #add a column to distinguish seasons
            df_yr['year'] = year
            #clean column strings for concat
            df_yr.columns = [x.lower().strip() for x in df_yr.columns]
            #add year dataframe to overall dataframe
            df_all = pd.concat([df_all, df_yr])
        
        return df_all

# create dictionary for dataframes based on info type
dict_dfs = {'AVG':'', 'ERA':'', 'C':''}
#loop through dictionary to create dataframes
for k,v in dict_dfs.items():
    dict_dfs[k] = combine_years(2011, 2023, k)
    clean_team(dict_dfs[k])
# store dataframes as variables
df_avg = dict_dfs['AVG']
df_era = dict_dfs['ERA']
df_c = dict_dfs['C']


#test plot 
sns.set_theme(style="darkgrid")
#all batting averages over the years
sns.relplot(df_avg[df_avg.team != 'Totals'], x='year', y='avg', kind='line', 
            hue='team', style='team', dashes=False, markers=True, height=6, aspect=1.5)
plt.show()
