#!/usr/bin/env python3

import json
import pdb
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from collections import OrderedDict
import os.path
import xlsxwriter
import pandas as pd

print ("Merge Teams Tool")
print ("**************************")
file = 'json/bracket.json'
if (not os.path.exists(file)):
    print ("brackets file is missing, run the scrape_bracket tool to create")
    exit()
with open(file) as bracket_file:
    dict_bracket = json.load(bracket_file, object_pairs_hook=OrderedDict)

file = 'json/stats.json'
if (not os.path.exists(file)):
    print ("statistics file is missing, run the scrape_stats tool to create")
    exit()
with open(file) as stats_file:
    dict_stats = json.load(stats_file, object_pairs_hook=OrderedDict)

AllTeams=[]
for item in dict_bracket.values():
    AllTeams.append(item["TeamA"])
    AllTeams.append(item["TeamB"])
team_set = set(AllTeams)
bracket_teams = list(team_set)
bracket_teams.sort()

AllTeams=[]
for item in  dict_stats.values():
    AllTeams.append(item["Team"])
team_set = set(AllTeams)
stats_teams = list(team_set)
stats_teams.sort()

dict_merge = OrderedDict()
dict_merge["bracket team"] = []
dict_merge["stats team"] = []
dict_merge["ratio"] = []
dict_merge["fixed stats team"] = []
values = []
IDX = []
index=0
for item in bracket_teams:
    index+=1
    IDX.append(index)
    dict_merge["bracket team"].append(item)
    statskey = process.extractOne(item, stats_teams, scorer=fuzz.token_sort_ratio)
    dict_merge["stats team"].append(statskey[0])
    dict_merge["ratio"].append(statskey[1])
    dict_merge["fixed stats team"].append("")
    values.append([item,statskey[0],statskey[1],""])

df=pd.DataFrame(IDX, columns=['Index'])
df['Index']=IDX
df['bracket team'] = dict_merge["bracket team"]
df['stats team'] = dict_merge["stats team"]
df['ratio'] = dict_merge["ratio"]
df['fixed stats team']=dict_merge["fixed stats team"]

print ("... creating merge excel spreadsheet")
excel_file = "merge.xlsx"
writer = pd.ExcelWriter(excel_file, engine="xlsxwriter")
df.to_excel(writer, sheet_name="Sheet1", index=False)
writer.close()

print ("done.")
