#!/usr/bin/env python3

import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import html5lib
import pdb
from scipy.stats import norm
from collections import OrderedDict

def FindMergeTeams(teama, teamb, dict_merge):
    FoundA = ""
    FoundB = ""
    for index in range(len(dict_merge["Index"])):
        idx = str(index)
        if (teama == dict_merge["bracket team"][idx]):
            FoundA = dict_merge["stats team"][idx]
            if (dict_merge["fixed stats team"][idx]):
                FoundA = dict_merge["fixed stats team"][idx]
        if (teamb == dict_merge["bracket team"][idx]):
            FoundB = dict_merge["stats team"][idx]
            if (dict_merge["fixed stats team"][idx]):
                FoundB = dict_merge["fixed stats team"][idx]
        if (FoundA and FoundB):
            break
    if (FoundA == "" or FoundB == ""):
        if (teama != "?" or teamb != "?"):
            print ("warning, in FindTeams() both teams not found, correct your merge spreadsheet, please")
            print ("*** TeamA: [{0}:{1}], TeamB: [{2}:{3}] ***".format(teama, FoundA, teamb, FoundB))
    return FoundA, FoundB

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

def Chance(teama, teamb, neutral, verbose):
    EffMgn = Line(teama, teamb, neutral, verbose)
    if verbose:
        print ("Chance(efficiency margin) {0}".format(EffMgn))
    bPercent = norm.cdf(0, EffMgn, 11)
    aPercent = 1.0 - bPercent
    aPercent = int(round(aPercent * 100.0))
    bPercent = int(round(bPercent * 100.0))
    if verbose:
        print ("Chance({0}) {1}%".format(teama["Team"], aPercent), "vs. Chance({0}) {1}%".format(teamb["Team"], bPercent))
    return aPercent, bPercent

def Tempo(teama, teamb, verbose):
    Tdiff = (float(teama['AdjT']) + float(teamb['AdjT'])) / 200.0
    if verbose:
        print ("Tempo(tempo) {0}".format(Tdiff * 100))
    return Tdiff

def Test(verbose):
    result = 0
    # Purdue, Northwestern on 3/5/17
    # Actual Score: Edwards leads No. 16 Purdue past Northwestern, 69-65
    # venue was: Welsh-Ryan Arena in Evanston, IL (Northwestern was the home team)
    teama = {'Team':"purdue", 'AdjEM':24.31, 'AdjT':69.5, 'Result1':57, 'Result2':69}
    teamb = {'Team':"northwestern", 'AdjEM':15.83, 'AdjT':65.8, 'Result1':43,'Result2':67}
    if verbose:
        print (teama)
        print (teamb)
    print ("Test #1 Purdue at Northwestern on 3/5/17")
    print ("        Northwestern is Home team, testing Chance() routine)")
    chancea, chanceb =  Chance(teama, teamb, False, verbose)
    if (teama['Result1'] == chancea):
        result += 1
    if (teamb['Result1'] == chanceb):
        result += 1
    if (result == 2):
        print ("Test #1 - pass")
    print (" ")
    print ("Test #2 Purdue at Northwestern on 3/5/17")
    print ("        Northwestern is Home team, testing Score() routine)")
    print ("                    Actual Score: Edwards lead No. 16 Purdue past Northwestern, 69-65")
    scorea, scoreb = Score(teama, teamb, False, verbose)
    if (teama['Result2'] == scorea):
        result += 1
    if (teamb['Result2'] == scoreb):
        result += 1
    if (result == 4):
        print ("Test #2 - pass")
        return True
    return False

def Score(teama, teamb, neutral, verbose):
    tempo = Tempo(teama, teamb, verbose)
    EffMgn = Line(teama, teamb, neutral, verbose)
    if verbose:
        print ("Score(efficiency margin) {0}".format(EffMgn))
    bScore = int(round((tempo * 100) - (EffMgn / 2.0)))
    aScore = int(round((tempo * 100) + (EffMgn / 2.0)))
    if verbose:
        print ("Score({0}) {1}".format(teama["Team"], aScore), "vs. Score({0}) {1}".format(teamb["Team"], bScore))
    return aScore, bScore

def Line(teama, teamb, neutral, verbose):
    tempo = Tempo(teama, teamb, verbose)
    if verbose:
        print ("Line(tempo) {0}".format(tempo * 100))
    EMdiff = (float(teama['AdjEM']) - float(teamb['AdjEM'])) * tempo
    EffMgn = 0
    if neutral:
        EffMgn = EMdiff
    else:
        EffMgn = EMdiff - 3.75
    if verbose:
        print ("Line(efficiency margin) {0}".format(EffMgn))
    return EffMgn

def Calculate(first, second, neutral, verbose):
    if verbose:
        if neutral:
            info = "{0} verses {1} at a neutral location".format(first, second)
            print (info)
        else:
            info = "Visiting team: {0} verses Home team: {1}".format(first, second)
            print (info)

    teama, teamb = findTeams(first, second)
    if (not teama or not teamb):
        return {}
    chancea, chanceb =  Chance(teama, teamb, neutral, verbose)
    scorea, scoreb = Score(teama, teamb, neutral, verbose)
    line = Line(teama, teamb, neutral, verbose)
    tempo = Tempo(teama, teamb, verbose)
    dict_score = \
    {
        'teama':first, 'scorea':"{0}".format(scorea), 'chancea':"{0}%".format(chancea) \
        ,'teamb':second, 'scoreb':"{0}".format(scoreb), 'chanceb':"{0}%".format(chanceb), \
        'line':int(round(line)), 'tempo':"{0}".format(int(round(tempo * 100))) \
    }
    if verbose:
        print ("Calculate(dict_score) {0}".format(dict_score))
    return dict_score
