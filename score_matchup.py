#!/usr/bin/env python3

import sys, getopt
import os.path
import pdb
from datetime import datetime
from yad import YAD
import pandas as pd
from collections import OrderedDict
import json

import pyMadness

def CurrentStatsFile(filename):
    stat = os.path.getmtime(filename)
    stat_date = datetime.fromtimestamp(stat)
    if stat_date.date() < datetime.now().date():
        return False
    return True

def RefreshStats():
    import scrape_stats

def GetTeams():
    teams=[]
    print("... retrieving stats file")
    if (not os.path.exists("json/stats.json")):
        print ("stats file is missing, run the scrape_stats tool to create")
        exit()
    with open("json/stats.json") as stat_file:
        dict_stats = json.load(stat_file, object_pairs_hook=OrderedDict)
    for item in dict_stats:
        teams.append('"' + dict_stats[item]["Team"] + '"')
    team_set = set(teams)
    teams = list(team_set)
    teams.sort()
    return teams
    
def GetYAD():
    inputs={}
    yad = YAD()
    teams = GetTeams()
    away_team = yad.Entry(title="Basketball Predictor", label="Away Team", use_completion=True, data=teams)
    home_team = yad.Entry(title="Basketball Predictor", label="Home Team", use_completion=True, data=teams)
    data = "LBL:{0}\nCHK:Verbose:false\nCHK:Neutral Court:false".format(away_team + "@" + home_team)
    final_screen = yad.Form(title="Basketball Predictor", use_completion=True, align="center", fields=data)
    first = away_team
    second = home_team
    verbose = final_screen[1]
    neutral = final_screen[2]
    inputs["first"] = first
    inputs["second"] = second
    inputs["verbose"] = verbose
    inputs["neutral"] = neutral
    return inputs

def main(argv):
    first = ""
    second = ""
    neutral = False
    test = False
    verbose = False
    try:
        opts, args = getopt.getopt(argv, "hf:sntv", ["help", "first=", "second=", "neutral","test","verbose"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    output = None
    for o, a in opts:
        if o in ("-n", "--neutral"):
            neutral = True
        elif o in ("-t", "--test"):
            test = True
        elif o in ("-v", "--verbose"):
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit
        elif o in ("-f", "--first"):
            first = a
        elif o in ("-s", "--second"):
            second = a
        else:
            assert False, "unhandled option"
    if verbose:
        print (" ")
        print ("increased information level")
        print ("Score Matchup Tool")
        print ("**************************")
        usage()
        print ("**************************")
    if (test):
        testResult = pyMadness.Test(verbose)
        if (testResult):
            print ("Test result - pass")
        else:
            print ("Test result - fail")
    else:
        if (not first and not second):
            yad_inputs = GetYAD()
            if yad_inputs:
                first = yad_inputs["first"]
                second = yad_inputs["second"]
                verbose = yad_inputs["verbose"]
                neutral = yad_inputs["neutral"]
            else:
                print ("Score Matchup Tool")
                print ("**************************")
                usage()
                print ("**************************")
                exit()
        file = "json/stats.json"
        if (not CurrentStatsFile(file)):
            RefreshStats()
        ds = {}
        ds = pyMadness.Calculate(first, second, neutral, verbose)
        if (not ds):
            print ("Could not predict this matchup?")
            exit()
        if (neutral):
            print ("{0} {1} vs {2} {3} {4}-{5}".format(ds["teama"], ds["chancea"], ds["teamb"], ds["chanceb"],
                ds["scorea"], ds["scoreb"]))
        else:
            print ("{0} {1} at {2} {3} {4}-{5}".format(ds["teama"], ds["chancea"], ds["teamb"], ds["chanceb"],
                ds["scorea"], ds["scoreb"]))

def usage():
    usage = """
    -h --help                 Prints this
    -f --first                First Team (The Away Team)
    -s --second               Second Team (The Home Team)
    -n --neutral              Playing on a neutral Field
    -t --test                 runs test routine to check calculations
    -v --verbose              increase information level
    """
    print (usage) 

if __name__ == "__main__":
  main(sys.argv[1:])
