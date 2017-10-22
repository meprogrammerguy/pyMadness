#!/usr/bin/env python3

import json
import pdb
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv
from collections import OrderedDict
import os.path

print ("Merge Teams Tool")
print ("**************************")
file = 'espn.json'
if (not os.path.exists(file)):
    print ("brackets file is missing, run the scrape_espn tool to create")
    exit()
with open(file) as espn_file:
    dict_espn = json.load(espn_file, object_pairs_hook=OrderedDict)

file = 'kenpom.json'
if (not os.path.exists(file)):
    print ("statistics file is missing, run the scrape_kenpom tool to create")
    exit()
with open(file) as kenpom_file:
    dict_kenpom = json.load(kenpom_file, object_pairs_hook=OrderedDict)

AllTeams=[]
for item in dict_espn.values():
    AllTeams.append(item["TeamA"])
    AllTeams.append(item["TeamB"])
team_set = set(AllTeams)
espn_teams = list(team_set)
espn_teams.sort()

AllTeams=[]
for item in  dict_kenpom.values():
    AllTeams.append(item["Team"])
team_set = set(AllTeams)
kenpom_teams = list(team_set)
kenpom_teams.sort()

merge_sheet = open('merge.csv', 'w')
csvwriter = csv.writer(merge_sheet)
dict_merge = OrderedDict()
dict_merge["espn team"] = []
dict_merge["kenpom team"] = []
dict_merge["ratio"] = []
dict_merge["override team"] = []
values = []
for item in espn_teams:
    dict_merge["espn team"].append(item)
    kenpomkey = process.extractOne(item, kenpom_teams, scorer=fuzz.token_sort_ratio)
    dict_merge["kenpom team"].append(kenpomkey[0])
    dict_merge["ratio"].append(kenpomkey[1])
    dict_merge["override team"].append("")
    values.append([item,kenpomkey[0],kenpomkey[1],""])

csvwriter.writerow(dict_merge.keys())
for value in values:
    csvwriter.writerow(value)
merge_sheet.close()
print ("done.")
