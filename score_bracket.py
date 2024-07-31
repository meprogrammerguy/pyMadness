#!/usr/bin/env python3

import sys, getopt
import pyMadness
from collections import OrderedDict
import json
import pdb
import os.path
import pandas as pd
from datetime import datetime
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
    stat_file = "json/stats.json"
    bracket_file = "json/bracket.json"
    merge_file = "merge.xlsx"
    output_file = "predict.xlsx"
    input_file = "predict.xlsx"
    test = False
    verbose = False
    try:
        opts, args = getopt.getopt(argv, "hs:b:m:o:itv", ["help", "stat_file=", "bracket_file=", \
            "merge_file=", "output_file=", "input_file=", "verbose", "test"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    output = None
    for o, a in opts:
        if o in ("-t", "--test"):
            test = True
        elif o in ("-v", "--verbose"):
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit
        elif o in ("-s", "--stat_file"):
            stat_file = a
        elif o in ("-b", "--bracket_file"):
            bracket_file = a
        elif o in ("-m", "--merge_file"):
            merge_file = a
        elif o in ("-o", "--output_file"):
            output_file = a
        elif o in ("-i", "--input_file"):
            input_file = a
        else:
            assert False, "unhandled option"
    if (test):
        testResult = pyMadness.Test(verbose)
        if (testResult):
            print ("Test result - pass")
        else:
            print ("Test result - fail")
    else:
        PredictTournament(stat_file, bracket_file, merge_file, input_file, output_file, verbose)
    print ("{0} has been created.".format(output_file))
    print ("done.")
    
def usage():
    usage = """
    -h --help                 Prints this help
    -s --stat_file            stats file                      (json file format)
    -b --bracket_file         bracket file                    (json file format)
    -m --merge_file           merge file                      (excel spreadsheet file format)
    -i --input_file           input file gets pick overrides  (excel spreadsheet file format)
    -o --output_file          output file                     (excel spreadsheet file format)
    -t --test                 runs test routine to check calculations
    -v --verbose              increase the information level
    """
    print (usage) 

def PredictTournament(stat_file, bracket_file, merge_file, input_file, output_file, verbose):
    print ("Tournament Prediction Tool")
    print ("**************************")
    print ("Statistics file: {0}".format(stat_file))
    if verbose:
        print (" ")
        print ("increased information level")
        print ("Score Bracket Tool")
        print ("**************************")
        usage()
        print ("**************************")
    print ("Brackets   file: {0}".format(bracket_file))
    print ("Team Merge file: {0}".format(merge_file))
    print ("Input      file: {0}".format(input_file))
    print ("Output     file: {0}".format(output_file))
    print ("**************************")
    picks = []
    if (os.path.exists(input_file)):
        print("... retrieving prediction spreadsheet")
        excel_df = pd.read_excel(input_file, sheet_name='Sheet1')
        predict_json = json.loads(excel_df.to_json())
        for x in range(len(predict_json["Index"])):
            pick = predict_json["Pick"][str(x)]
            sa =  predict_json["ScoreA"][str(x)]
            sb =  predict_json["ScoreB"][str(x)]
            idx = predict_json["Index"][str(x)]
            if (sa >= sb and pick == "TeamB"):
                picks.append([idx, pick])
            else:
                if (sa < sb and pick == "TeamA"):
                    picks.append([idx, pick])
    if (len(picks) == 0):
        print ("No pick Overrides")
    elif (len(picks) == 1):
        print ("Overriding one calculated pick")
    else:
        print ("Overriding {0} calculated pick(s)".format(len(picks)))

    if (not os.path.exists(merge_file)):
        print ("merge spreadsheet is missing, run the merge_teams tool to create")
        exit() 

    dict_merge={}
    excel_df = pd.read_excel(merge_file, sheet_name='Sheet1')
    dict_merge = json.loads(excel_df.to_json())

    if (not os.path.exists(bracket_file)):
        print ("madness bracket is missing, run the scrape_bracket tool to create")
        exit()
    dict_bracket={}
    with open(bracket_file) as bracket_file:
        dict_bracket = json.load(bracket_file, object_pairs_hook=OrderedDict)
   
    for itm in dict_bracket.values():
        teama, teamb = pyMadness.FindMergeTeams(itm["TeamA"], itm["TeamB"], dict_merge)
        itm["TeamA"] = teama
        itm["TeamB"] = teamb
        
    if (not CurrentStatsFile(stat_file)):
        RefreshStats()
    if (not os.path.exists(stat_file)):
        print ("statistics file is missing, run the scrape_stats tool to create")
        exit()
        
    with open(stat_file) as stat_file:
        dict_stats = json.load(stat_file, object_pairs_hook=OrderedDict)

    dict_predict = []
    dict_predict = LoadPredict(dict_predict, dict_bracket)
    for rnd in range(0, 7):
        dict_predict = PredictRound(rnd, dict_predict, verbose)
        if rnd < 6:
            dict_predict = PromoteRound(rnd, dict_predict, picks)
                
    A=[]
    B=[]
    C=[]
    D=[]
    E=[]
    F=[]
    G=[]
    H=[]
    I=[]
    J=[]
    K=[]
    IDX=[]
    for item in dict_predict:
        IDX.append(item[0])
        A.append(item[1])
        B.append(item[2])
        C.append(item[3])
        D.append(item[4])
        E.append(item[5])
        F.append(item[6])
        G.append(item[7])
        H.append(item[8])
        I.append(item[9])
        J.append(item[10])
        K.append(item[11])
    
    df=pd.DataFrame(IDX, columns=['Index'])
    df['Index']=IDX
    df['SeedA'] = A
    df['TeamA'] = B
    df['ChanceA'] = C
    df['ScoreA'] = D
    df['SeedB'] = E
    df['TeamB'] = F
    df['ChanceB'] = G
    df['ScoreB'] = H
    df['Region'] = I
    df['Round'] = J
    df['Pick'] = K

    print ("... creating prediction spreadsheet")
    writer = pd.ExcelWriter(output_file, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Sheet1", index=False)
    writer.close()

def LoadPredict(dict_predict, dict_bracket):
    index = 0
    for rnd in range(0, 7):
        for item in dict_bracket:
            index += 1
            brk = dict_bracket[item]
            if brk["Round"] == rnd:
                if brk["Round"] <= 1:
                    dict_predict.append([brk["Index"], brk["SeedA"], brk["TeamA"], "?%", "?", \
                        brk["SeedB"], brk["TeamB"], "?%", "?", brk["Region"], brk["Round"], "?", \
                        brk["Next Match"], brk["Next Slot"]])
                else:
                    dict_predict.append([brk["Index"], "?", "?", "?%", "?", "?", "?", "?%", "?", \
                        brk["Region"], brk["Round"], "?", brk["Next Match"], brk["Next Slot"]])
    return dict_predict

def PredictRound(rnd, dict_predict, verbose):
    index=0
    for item in dict_predict:
        idx = dict_predict[index][0]
        if item[10] == rnd:
            dict_score = pyMadness.Calculate(item[2], item[6], True, verbose)
            if "scorea" in dict_score:
                item[3] = dict_score["chancea"]
                item[4] = dict_score["scorea"]
                item[7] = dict_score["chanceb"]
                item[8] = dict_score["scoreb"]
                if (item[4] >= item[8]):
                    item[11] = "TeamA"
                else:
                    item[11] = "TeamB"
        index+=1            
    return dict_predict
        
def FindOverrides(i, p, orig):
    pick = orig
    for item in p:
        if item[0] == i:
            pick = item[1]
            break
    return pick
    
def PromoteRound(rnd, dict_predict, picks):
    for item in dict_predict:
        if rnd == item[10]:
            index = item[12]
            for promote in dict_predict:
                if promote[0] == index:
                    override = FindOverrides(item[0], picks, item[11])
                    if override != item[11]:
                        print ("picking {0} in round {1} in match {2} ** {3} vs {4}" \
                            .format(override, item[10], item[0], item[2], item[6]))
                        item[11] = override
                    if item[11] == "TeamA":
                        if item[13] == 1:   # slot
                            promote[1] = item[1]
                            promote[2] = item[2]
                        else:
                            promote[5] = item[1]
                            promote[6] = item[2]
                    else:
                        if item[13] == 1:
                            promote[1] = item[5]
                            promote[2] = item[6]
                        else:
                            promote[5] = item[5]
                            promote[6] = item[6]
    return dict_predict
    
if __name__ == "__main__":
    main(sys.argv[1:])
