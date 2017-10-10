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

def Chance(teama, teamb, std = 11.5, homeAdvantage = 3.75, homeTeam = 'none', verbose = True):
    Tdiff = (float(teama['AdjT']) + float(teamb['AdjT'])) / 200.0
    if (verbose):
        print ("Chance(tempo) {0}".format(Tdiff * 100))
    EMdiff = (float(teama['AdjEM']) - float(teamb['AdjEM'])) * Tdiff
    if (verbose):
        print ("Chance(efficiency margin) {0}".format(EMdiff))
    if homeTeam == teama["Team"]:
        bPercent = norm.cdf(0, EMdiff + homeAdvantage, std)
    elif homeTeam == teamb["Team"]:
        bPercent = norm.cdf(0, EMdiff - homeAdvantage, std)
    else:
        bPercent = norm.cdf(0, EMdiff, std)
    aPercent = 1.0 - bPercent
    if (verbose):
        print ("Chance(teama) {0}".format(aPercent), "Chance(teamb) {0}".format(bPercent))
    return aPercent, bPercent

def Tempo(teama, teamb, verbose = True):
    Tdiff = (float(teama['AdjT']) + float(teamb['AdjT'])) / 200.0
    if (verbose):
        print ("Tempo(tempo) {0}".format(Tdiff * 100))
    return Tdiff

def Test(verbose):
    if (verbose):
        print ("verbose")
    return False

def Score(teama, teamb, verbose = True, AVGnational = 100, AVGtempo = 67.3):
    Tdiff = (float(teama['AdjT']) + float(teamb['AdjT'])) / 200.0
    Tdiff *= Tdiff * 100.0 / AVGtempo
    pointsTeama = float(teama['AdjO']) / 100.0 * float(teamb['AdjD']) / 100.0 * AVGnational * Tdiff
    pointsTeamb = float(teamb['AdjO']) / 100.0 * float(teama['AdjD']) / 100.0 * AVGnational * Tdiff
    if (verbose):
        print ("Score(Teama) {0}".format(pointsTeama),"Score(Teamb) {0}".format(pointsTeamb))
    return pointsTeama, pointsTeamb

def Calculate(first, second, neutral, verbose):
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
        chancea, chanceb =  Chance(teama, teamb, homeTeam = teamb["Team"], verbose = verbose)
    else:
        chancea, chanceb =  Chance(teama, teamb, verbose = verbose)
    tempo = Tempo(teama, teamb, verbose = verbose)
    scorea, scoreb = Score(teama, teamb, verbose = verbose)
    #pdb.set_trace()

    dict_score = {'teama':first, 'scorea':"{0}".format(int(round(scorea))), 'chancea':"{0}%".format(int(round(chancea * 100))) ,'teamb':second, 'scoreb':"{0}".format(int(round(scoreb))), 'chanceb':"{0}%".format(int(round(chanceb * 100))), 'line':1, 'tempo':"{0}".format(int(round(tempo * 100))) }
    if (verbose):
        print ("Calculate(dict_score) {0}".format(dict_score))
    pdb.set_trace()
    return dict_score
