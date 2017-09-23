#!/usr/bin/env python3
import json
import pdb
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from lxml import etree as ET

file = 'espn.json'
with open(file) as espn_file:
    dict_espn = json.load(espn_file)

file = 'kenpom.json'
with open(file) as kenpom_file:
    dict_kenpom = json.load(kenpom_file)

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

root = ET.Element("root")
for item in espn_teams:
    merge = ET.SubElement(root, "merge")
    ET.SubElement(merge, "bracket_key", name="team").text = item
    kenpomkey = process.extractOne(item, kenpom_teams, scorer=fuzz.token_sort_ratio)
    ET.SubElement(merge, "token_sort_key", name="team").text = kenpomkey[0]
    ET.SubElement(merge, "token_sort_value", name="ratio").text = str(kenpomkey[1])
    ET.SubElement(merge, "override_key", name="team").text = ""

tree = ET.ElementTree(root)
tree.write("merge_teams.xml", pretty_print=True)
