#import modules
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

year = 2012
dict_dfs = {}
dict_dfs.keys = ['AVG', 'ERA', 'C']
for k,v in dict_dfs.items():
    filename = f"MEAC-{year}-{k}.csv"
    v = pd.read_csv(filename)
df_avg = dict_dfs['AVG']
df_era = dict_dfs['ERA']
df_c = dict_dfs['C']
print(df_avg.head())
