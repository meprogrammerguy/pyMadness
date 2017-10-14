#!/usr/bin/env python3

import sys, getopt
import pyMadness

def main(argv):
    stat_file = "kenpom.json"
    bracket_file = "espn.json"
    merge_file = "merge.csv"
    output_file = "predict.csv"
    verbose = False
    test = False
    try:
        opts, args = getopt.getopt(argv, "hs:b:m:o:vt", ["help", "stat_file=", "bracket_file=", "merge_file=", "output_file=", "verbose", "test"])
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
        PredictTournament(stat_file, bracket_file, merge_file, output_file, verbose)
        print ("done.")

def usage():
    usage = """
    -h --help                 Prints this
    -v --verbose              Increases the information level
    -s --stat_file            stats file   (json file format)
    -b --bracket_file         bracket file (json file format)
    -m --merge_file           merge file   (csv/spreadsheet file format)
    -o --output_file          output file  (csv/spreadsheet file format)
    -t --test                 runs test routine to check calculations
    """
    print (usage) 

def PredictTournament(stat_file, bracket_file, merge_file, output_file, verbose):
    if (verbose):
        print ("Tournament Prediction Tool")
        print ("**************************")
        print ("Statistics file: {0}".format(stat_file))
        print ("Brackets   file: {0}".format(bracket_file))
        print ("Team Merge file: {0}".format(merge_file))
        print ("Output     file: {0}".format(output_file))
        print ("**************************")

if __name__ == "__main__":
  main(sys.argv[1:])
