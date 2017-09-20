#!/usr/bin/env python
import json
import pdb

file = 'espn.json'
with open(file) as espn_file:
    dict_espn = json.load(espn_file)

file = 'kenpom.json'
with open(file) as kenpom_file:
    dict_kenpom = json.load(kenpom_file)

