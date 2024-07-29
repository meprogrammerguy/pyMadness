#!/usr/bin/env python3

import sys, getopt
import os, os.path
import pdb
from datetime import datetime
import pandas as pd
from collections import OrderedDict
import json
from pynotifier import NotificationClient, Notification
from pynotifier.backends import platform

import pyMadness

def CurrentStatsFile(filename):
    stat = os.path.getmtime(filename)
    stat_date = datetime.fromtimestamp(stat)
    if stat_date.date() < datetime.now().date():
        return False
    return True

def RefreshStats():
    import scrape_stats
    
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
            answer = "{0} {1} vs {2} {3} {4}-{5}".format(ds["teama"], ds["chancea"], ds["teamb"], ds["chanceb"],
                ds["scorea"], ds["scoreb"])
        else:
            answer = "{0} {1} at {2} {3} {4}-{5}".format(ds["teama"], ds["chancea"], ds["teamb"], ds["chanceb"],
                ds["scorea"], ds["scoreb"])
        print (answer)
        cwd = os.getcwd()
        madness_icon = '{0}/basketball.ico'.format(cwd)
        c = NotificationClient()
        c.register_backend(platform.Backend())
        notification = Notification(title='pyMadness Predictor', message=answer,\
            icon_path=madness_icon, duration=20)
        c.notify_all(notification)

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
