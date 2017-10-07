#!/usr/bin/env python3

import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import html5lib
import pdb
from scipy.stats import norm
import pylab as p
import numpy as np

def predictScore(first, second, neutral, verbose):
    if (verbose):
        if (neutral):
            info = "{0} verses {1} at a neutral location".format(first, second)
            print (info)
        else:
            info = "Home team: {0} verses Visiting team: {1}".format(first, second)
            print (info)

    file = 'kenpom.json'
    with open(file) as kenpom_file:
        dict_kenpom = json.load(kenpom_file)
    teama = {}
    teamb = {}
    count = 0
    for item in dict_kenpom.values():
        if (item["Team"] == first):
            teama = item
            count += 1
        if (item["Team"] == second):
            teamb = item
            count += 1
        if (count == 2):
            break
    if (verbose and count < 2):
        if (not teama):
            print ("Could not find stats for {0}".format(first))
        if (not teamb):
            print ("Could not find stats for {0}".format(second))
        return {}
    #PointDiff = (AdjEM_A - AdjEM_B)*(AdjT_A + AdjT_B)/200
    # Gonzaga, Villanova on 10/7/17
    kpEMa, kpEMb = 32.05, 29.88
    kpTa, kpTb = 70.1, 64.0
    homeadv = 3.5
    kpEMtempo = (kpTa + kpTb)/200
    # Number of points A should win by on neutral floor
    kpEMdiff = (kpEMa - kpEMb)*kpEMtempo
    # Number of points A should win by on oponents floor
    if (not neutral):
        kpEMdiff = (kpEMa - kpEMb)*kpEMtempo - homeadv

    pointDiff = (float(teama["AdjEM"]) - float(teamb["AdjEM"])) * (float(teama["AdjT"]) + float(teamb["AdjT"])) / 200
    if (not neutral):
        pointDiff += homeadv
    stdev = 11

    chancea = norm.cdf(0, kpEMdiff, stdev)
    chanceb = 1 - chancea


    dict_score = {'scorea':1, 'chancea':"{0:6.4f}%".format(chancea * 100) ,'scoreb':1, 'chanceb':"{0:6.4f}%".format(chanceb * 100), 'line':1, 'tempo':1 }
    if (verbose):
        print (dict_score)
    pdb.set_trace()
    return dict_score
