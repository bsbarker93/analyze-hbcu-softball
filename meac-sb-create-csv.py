#import modules
import pandas as pd
import re
import os
import requests
from bs4 import BeautifulSoup


def list_to_csv(filename, aList):
    abs_path = os.path.dirname(__file__)
    rel_path = "./data/"+filename
    with open(os.path.join(abs_path, rel_path), "w") as file:
        file.writelines(aList)
        file.close()
    return

def team_stats(year):
    url = f"https://static.meacsports.com/custompages/stats/softball/{year}/lgteams.htm"
    r = requests.get(url)
    tbl = BeautifulSoup(r.text.encode('utf-8'), features="html.parser").find_all('table')
    if len(tbl) != 0:
        for table in tbl[1:6:2]:
            filename = f'MEAC-{year}-{str.strip(table.find_all('td')[1].text).upper()}.csv'
            lst2 = []
            for row in table.find_all('tr'):
                data = [str.strip(x.text) for x in row.find_all('td')]
                strRow = ", ".join(data)+"\n"
                lst2.append(strRow)
            list_to_csv(filename, lst2)
    else:
        txt = BeautifulSoup(r.text.encode('utf-8'), features="html.parser").find_all('font')[2].text
        tables = re.split(r"\(.+\)", txt)
        for table in tables:
            lst = [x for x in re.split(r"\r\n+", table) if x] 
            lst[0] = re.sub(r"\s+", ",", str.strip(lst[0]))
            filename = f'MEAC-{year}-{re.split(",", lst[0])[1]}.csv'
            data = [re.sub(r"(?<=[\d\.])\s+", ",", str.strip(line))+"\n" for line in lst]
            list_to_csv(filename, data)
    return

years = [2010, 2011, 2012]
for year in years:
    team_stats(year)
