#!/usr/bin/env python3

import sys, getopt
import pyMadness
from collections import OrderedDict
import json
import csv
import pdb

def main(argv):
    stat_file = "kenpom.json"
    bracket_file = "espn.json"
    merge_file = "merge.csv"
    output_file = "predict.csv"
    verbose = False
    test = False
    gamepredict = False
    try:
        opts, args = getopt.getopt(argv, "hs:b:m:o:vtg", ["help", "stat_file=", "bracket_file=", "merge_file=", "output_file=", "verbose", "test", "gamepredict"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o in ("-v", "--verbose"):
            verbose = True
        elif o in ("-t", "--test"):
            test = True
        elif o in ("-g", "--gamepredict"):
            gamepredict = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit
        elif o in ("-s", "--stat_file"):
            stat_file = a
        elif o in ("-b", "--bracket_file"):
            bracket_file = a
        elif o in ("-b", "--merge_file"):
            merge_file = a
        elif o in ("-o", "--output_file"):
            output_file = a
        else:
            assert False, "unhandled option"
    if (test):
        testResult = pyMadness.Test(verbose)
        if (testResult):
            print ("Test result - pass")
        else:
            print ("Test result - fail")
    else:
        PredictTournament(stat_file, bracket_file, merge_file, output_file, verbose, gamepredict)
        print ("done.")

def usage():
    usage = """
    -h --help                 Prints this
    -v --verbose              Increases the information level
    -s --stat_file            stats file   (json file format)
    -b --bracket_file         bracket file (json file format)
    -m --merge_file           merge file   (csv/spreadsheet file format)
    -o --output_file          output file  (csv/spreadsheet file format)
    -g --gamepredict          obtain data from gamepredict.us (default is False)
    -t --test                 runs test routine to check calculations
    """
    print (usage) 

def PredictTournament(stat_file, bracket_file, merge_file, output_file, verbose, gamepredict):
    if (verbose):
        print ("Tournament Prediction Tool")
        print ("**************************")
        print ("Statistics file: {0}".format(stat_file))
        print ("Brackets   file: {0}".format(bracket_file))
        print ("Team Merge file: {0}".format(merge_file))
        print ("Output     file: {0}".format(output_file))
        if (gamepredict):
            print (" ")
            print ("===> (data will come from gamepredict.us) <===")
            print (" ")
        print ("**************************")

    file = bracket_file
    with open(file) as espn_file:
        dict_espn = json.load(espn_file, object_pairs_hook=OrderedDict)
    file = stat_file
    with open(file) as kenpom_file:
        dict_kenpom = json.load(kenpom_file, object_pairs_hook=OrderedDict)
    file = merge_file
    dict_merge = []
    with open(file) as merge_file:
        reader = csv.DictReader(merge_file)
        for row in reader:
            dict_merge.append(row)
    #pdb.set_trace()
    dict_predict = []
    dict_predict = LoadRound(0, dict_predict, dict_espn) 
    predict_sheet = open(output_file, 'w')
    csvwriter = csv.writer(predict_sheet)
    count = 0
    for row in dict_predict.values():
        #pdb.set_trace()
        if (count == 0):
            header = row.keys()
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(row.values())
    predict_sheet.close()

if __name__ == "__main__":
  main(sys.argv[1:])
