#!/usr/bin/env python3

import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import html5lib
import pdb
from scipy.stats import norm
import pylab as p
import numpy as np

def findTeams(first, second, verbose = True, file = "kenpom.json"):
    teama = {}
    teamb = {}
    count = 0

    with open(file) as kenpom_file:
        dict_kenpom = json.load(kenpom_file)

    for item in dict_kenpom.values():
        if (item["Team"].lower() == first.lower()):
            teama = item
            count += 1
        if (item["Team"].lower() == second.lower()):
            teamb = item
            count += 1
        if (count == 2):
            break
    if (verbose and count < 2):
        if (not teama):
            print ("Could not find stats for {0}".format(first))
        if (not teamb):
            print ("Could not find stats for {0}".format(second))
        return {}, {}
    return teama, teamb

def percentChance(teama, teamb, std = 11.5, homeAdvantage = 3.75, homeTeam = 'none', verbose = True):
    Tdiff = (float(teama['AdjT']) + float(teamb['AdjT'])) / 200.0
    if (verbose):
        print ("percentChance() tempo: {0}".format(Tdiff * 100))
    EMdiff = (float(teama['AdjEM']) - float(teamb['AdjEM'])) * Tdiff
    if (verbose):
        print ("percentChance() efficiency margin: {0}".format(EMdiff))
    if homeTeam == teama["Team"]:
        bPercent = norm.cdf(0, EMdiff + homeAdvantage, std)
    elif homeTeam == teamb["Team"]:
        bPercent = norm.cdf(0, EMdiff - homeAdvantage, std)
    else:
        bPercent = norm.cdf(0, EMdiff, std)
    aPercent = 1.0 - bPercent
    return aPercent, bPercent

def Score(first, second, neutral, verbose):
    if (verbose):
        if (neutral):
            info = "{0} verses {1} at a neutral location".format(first, second)
            print (info)
        else:
            info = "Visiting team: {0} verses Home team: {1}".format(first, second)
            print (info)

    teama, teamb = findTeams(first, second, verbose = verbose)
    if (not teama or not teamb):
        return {}
    if (not neutral):
        chancea, chanceb =  percentChance(teama, teamb, homeTeam = teamb["Team"], verbose = verbose)
    else:
        chancea, chanceb =  percentChance(teama, teamb, verbose = verbose)
    #pdb.set_trace()

    dict_score = {'teama':first, 'scorea':1, 'chancea':"{0:6.4f}%".format(chancea * 100) ,'teamb':second, 'scoreb':1, 'chanceb':"{0:6.4f}%".format(chanceb * 100), 'line':1, 'tempo':1 }
    if (verbose):
        print (dict_score)
    pdb.set_trace()
    return dict_score
