#!/usr/bin/env python3

import sys, getopt
import pyMadness
from collections import OrderedDict
import json
import pdb
import csv
import os.path
import pandas as pd

def main(argv):
    stat_file = "json/stats.json"
    bracket_file = "json/bracket.json"
    merge_file = "merge.xlsx"
    output_file = "predict.xlsx"
    input_file = "predict.xlsx"
    test = False
    try:
        opts, args = getopt.getopt(argv, "hs:b:m:o:it", ["help", "stat_file=", "bracket_file=", \
            "merge_file=", "output_file=", "input_file=", "test"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    output = None
    for o, a in opts:
        if o in ("-t", "--test"):
            test = True
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
        testResult = pyMadness.Test()
        if (testResult):
            print ("Test result - pass")
        else:
            print ("Test result - fail")
    else:
        PredictTournament(stat_file, bracket_file, merge_file, input_file, output_file)
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
    """
    print (usage) 

def PredictTournament(stat_file, bracket_file, merge_file, input_file, output_file):
    print ("Tournament Prediction Tool")
    print ("**************************")
    print ("Statistics file: {0}".format(stat_file))
    print ("Brackets   file: {0}".format(bracket_file))
    print ("Team Merge file: {0}".format(merge_file))
    print ("Input      file: {0}".format(input_file))
    print ("Output     file: {0}".format(output_file))
    print ("**************************")
    list_picks = []
    if (os.path.exists(input_file)):
        print("... retrieving prediction spreadsheet")
        excel_df = pd.read_excel(input_file, sheet_name='Sheet1')
        predict_json = json.loads(excel_df.to_json())

    
    
    #if (os.path.exists(input_file)):
        #file = input_file
        #with open(file) as input_file:
            #reader = csv.DictReader(input_file)
            #for row in reader:
                #if (row["ChanceA"] >= row["ChanceB"] and row["Pick"] == "TeamB"):
                    #list_picks.append([row["Index"], row["Pick"]])
                #elif (row["ChanceA"] < row["ChanceB"] and row["Pick"] == "TeamA"):
                    #list_picks.append([row["Index"], row["Pick"]])
                    
    if (len(list_picks) == 0):
        print ("No pick Overrides")
    elif (len(list_picks) == 1):
        print ("Overriding one calculated pick")
    else:
        print ("Overriding {0} calculated pick(s)".format(len(list_picks)))

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
        teama, teamb = FindTeams(itm["TeamA"], itm["TeamB"], dict_merge)
        itm["TeamA"] = teama
        itm["TeamB"] = teamb
        
    if (not os.path.exists(stat_file)):
        print ("statistics file is missing, run the scrape_stats tool to create")
        exit()
        
    with open(stat_file) as stat_file:
        dict_stats = json.load(stat_file, object_pairs_hook=OrderedDict)

    dict_predict = []
    dict_predict = LoadPredict(dict_predict, dict_bracket)
    #for rnd in range(0, 6):
    for rnd in range(0, 1):
        dict_predict = PredictRound(dict_predict)
        dict_predict = PromoteRound(rnd, dict_predict, list_picks)
    
    IDX=[]
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
    index=0
    for item in dict_predict:
        index+=1
        IDX.append(index)
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
    excel_file = "predict.xlsx"
    writer = pd.ExcelWriter(excel_file, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Sheet1", index=False)
    writer.close()

def FindTeams(teama, teamb, dict_merge):
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

def LoadPredict(dict_predict, dict_bracket):
    index = 0
    for item in dict_bracket.values():
        index += 1
        if item["Round"] <= 1:
            dict_predict.append([index, item["SeedA"], item["TeamA"], "?%", "?", \
                item["SeedB"], item["TeamB"], "?%", "?", item["Region"], item["Round"], "?"])
        else:
            dict_predict.append([index, "?", "?", "?%", "?", "?", "?", "?%", "?", item["Region"], item["Round"], "?"])
    return dict_predict

def PredictRound(dict_predict):
    for item in dict_predict:
        print (item[2],item[6])
        dict_score = pyMadness.Calculate(item[2], item[6], True)
        if "chancea" in dict_score:
            item[3] = dict_score["chancea"]
            item[4] = dict_score["scorea"]
            item[7] = dict_score["chanceb"]
            item[8] = dict_score["scoreb"]
            if (item[3] >= item[7]):
                item[11] = "TeamA"
            else:
                item[11] = "TeamB"
        else:
            print ("Calculate failed")
            print (item[2],item[6])
            pdb.set_trace()
            
    return dict_predict

def PromoteRound(rnd, dict_predict, list_picks):
    for item in dict_predict:
        slot, index = GetNextIndex(item[0])
        if (index == 99):
            print ("should not get here?")
            break
        promote = []                
        for pick in list_picks:
            flip = False
            if (int(pick[0]) == int(item[0])):
                flip = True
                item[11] = pick[1]
                break
            if (item[3] >= item[7]):
                if (flip):
                    print ("picking {0} over {1} in round {2} in match {3}".format(item[6], item[2], item[10], item[0]))
                    promote.append([index, slot, item[5], item[6]])
                else:
                    promote.append([index, slot, item[1], item[2]])
            else:
                if (flip):
                    print ("picking {0} over {1} in round {2} in match {3}".format(item[2], item[6], item[10], item[0]))
                    promote.append([index, slot, item[1], item[2]])
                else:
                    promote.append([index, slot, item[5], item[6]])
        pdb.set_trace()
        for item in dict_predict:
            for team in promote:
                if (team[0] == item[0]):
                    if (team[1] == 1):
                        item[1] = team[2]
                        item[2] = team[3]
                    else:
                        item[5] = team[2]
                        item[6] = team[3]
    return dict_predict 

def GetNextIndex(index):
    # Hundreds position is slot number 1 or 2 rest of the number is the index
    next_slot = \
    [
        135, 235, 156, 256, 150, 250, 123, 223,                                 # First Four
        109, 209, 110, 210, 111, 211, 112, 212, 113, 213, 114, 214, 115, 215,   # EAST
        124, 224, 125, 225, 126, 226, 127, 227, 128, 228, 129, 229, 130, 230,   # SOUTH
        142, 242, 143, 243, 144, 244, 145, 245, 146, 246, 147, 247, 148, 248,   # WEST
        157, 257, 158, 258, 159, 259, 160, 260, 161, 261, 162, 262, 163, 263,   # MIDWEST
        131, 231, 133, 233                                                      # Final Four
    ]
    if index > len(next_slot):  # prevent index crash if next_slot is correct then this won't happen
        return 9, 99
    else:
        slot = int(next_slot[index - 1] / 100)
        return slot, (next_slot[index - 1] - (slot * 100))

if __name__ == "__main__":
    main(sys.argv[1:])
