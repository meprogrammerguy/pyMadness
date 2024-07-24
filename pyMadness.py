#!/usr/bin/env python3

import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import html5lib
import pdb
from scipy.stats import norm
from collections import OrderedDict

def findTeams(first, second, file = "json/stats.json"):
    teama = {}
    teamb = {}
    count = 0

    with open(file) as stats_file:
        dict_stats = json.load(stats_file, object_pairs_hook=OrderedDict)

    for item in dict_stats.values():
        if (item["Team"].lower().strip() == first.lower().strip()):
            teama = item
            count += 1
        if (item["Team"].lower().strip() == second.lower().strip()):
            teamb = item
            count += 1
        if (count == 2):
            break
    if (count < 2):
        if (not teama):
            print ("Could not find stats for {0}".format(first))
        if (not teamb):
            print ("Could not find stats for {0}".format(second))
        return {}, {}
    return teama, teamb

def Chance(teama, teamb, neutral):
    EffMgn = Line(teama, teamb, neutral)
    print ("Chance(efficiency margin) {0}".format(EffMgn))
    bPercent = norm.cdf(0, EffMgn, 11)
    aPercent = 1.0 - bPercent
    aPercent = int(round(aPercent * 100.0))
    bPercent = int(round(bPercent * 100.0))
    print ("Chance({0}) {1}%".format(teama["Team"], aPercent), "vs. Chance({0}) {1}%".format(teamb["Team"], bPercent))
    return aPercent, bPercent

def Tempo(teama, teamb):
    Tdiff = (float(teama['AdjT']) + float(teamb['AdjT'])) / 200.0
    print ("Tempo(tempo) {0}".format(Tdiff * 100))
    return Tdiff

def Test():
    result = 0
    # Purdue, Northwestern on 3/5/17
    # Actual Score: Edwards leads No. 16 Purdue past Northwestern, 69-65
    # venue was: Welsh-Ryan Arena in Evanston, IL (Northwestern was the home team)
    teama = {'Team':"purdue", 'AdjEM':24.31, 'AdjT':69.5, 'Result1':81, 'Result2':72}
    teamb = {'Team':"northwestern", 'AdjEM':15.83, 'AdjT':65.8, 'Result1':19,'Result2':63}
    print (teama)
    print (teamb)
    print ("Test #1 Purdue at Northwestern on 3/5/17")
    print ("        Northwestern is Home team, testing Chance() routine)")
    chancea, chanceb =  Chance(teama, teamb, False)
    if (teama['Result1'] == chancea):
        result += 1
    if (teamb['Result1'] == chanceb):
        result += 1
    if (result == 2):
        print ("Test #1 - pass")
    print ("Test #2 Purdue at Northwestern on 3/5/17")
    print ("        Northwestern is Home team, testing Score() routine)")
    print ("                    Actual Score: Edwards lead No. 16 Purdue past Northwestern, 69-65")
    scorea, scoreb = Score(teama, teamb, False)
    if (teama['Result2'] == scorea):
        result += 1
    if (teamb['Result2'] == scoreb):
        result += 1
    if (result == 4):
        print ("Test #2 - pass")
        return True
    return False

def Score(teama, teamb, neutral):
    tempo = Tempo(teama, teamb)
    EffMgn = Line(teama, teamb, neutral)
    print ("Score(efficiency margin) {0}".format(EffMgn))
    aScore = int(round((tempo * 100) + (EffMgn / 2.0)))
    bScore = int(round((tempo * 100) - (EffMgn / 2.0)))
    print ("Score({0}) {1}".format(teama["Team"], aScore), "vs. Score({0}) {1}".format(teamb["Team"], bScore))
    return aScore, bScore

def Line(teama, teamb, neutral):
    tempo = Tempo(teama, teamb)
    print ("Line(tempo) {0}".format(tempo * 100))
    EMdiff = (float(teama['AdjEM']) - float(teamb['AdjEM'])) * tempo
    EffMgn = 0
    if neutral:
        EffMgn = EMdiff
    else:
        EffMgn = EMdiff + 3.75
    print ("Line(efficiency margin) {0}".format(EffMgn))
    return EffMgn

def Calculate(first, second, neutral):
    if (neutral):
        info = "{0} verses {1} at a neutral location".format(first, second)
        print (info)
    else:
        info = "Visiting team: {0} verses Home team: {1}".format(first, second)
        print (info)

    teama, teamb = findTeams(first, second)
    if (not teama or not teamb):
        return {}
    chancea, chanceb =  Chance(teama, teamb, neutral)
    scorea, scoreb = Score(teama, teamb, neutral)
    line = Line(teama, teamb, neutral)
    tempo = Tempo(teama, teamb)
    dict_score = \
    {
        'teama':first, 'scorea':"{0}".format(scorea), 'chancea':"{0}%".format(chancea) \
        ,'teamb':second, 'scoreb':"{0}".format(scoreb), 'chanceb':"{0}%".format(chanceb), \
        'line':int(round(line)), 'tempo':"{0}".format(int(round(tempo * 100))) \
    }
    print ("Calculate(dict_score) {0}".format(dict_score))
    return dict_score
