#!/usr/bin/env python
import json
import pdb
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import lxml.etree
import lxml.builder    
from lxml import etree
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

#for item in espn_teams:
#    print (item, process.extractOne(item, kenpom_teams))


#pdb.set_trace()

root = ET.Element("root")
doc = ET.SubElement(root, "doc")

ET.SubElement(doc, "field1", name="blah").text = "some value1"
ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"
tree = ET.ElementTree(root)
tree.write("merge.xml", pretty_print=True)
