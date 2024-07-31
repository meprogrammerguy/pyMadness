#!/usr/bin/env python3

import json
import pdb
from collections import OrderedDict
import os.path
from pathlib import Path
from datetime import datetime
import re
import pandas as pd
import sys
import pyMadness

def GetNumber(item):
    idx = re.findall(r'\d+', str(item))
    if (len(idx) == 0):
        idx.append("-1")
    return int(idx[0])

def RefreshBracket():
    import scrape_bracket

def GetRoundCount(r, j):
    count = 0
    for x in range(len(j)):
        rnd = j[str(x)]["Round"]
        if rnd == r:
            count+=1
    return count
    
def GetWins(b, p):
    wins={}
    total_count=0
    for r in range(0, 7):
        count = 0
        for x in range(len(p["Index"])):
            rnd = p["Round"][str(x)]
            idx = p["Index"][str(x)]
            if rnd == r:
                count+=1
        total_count+=count
        wins[r] = count
    wins[7] = total_count
    print ("wins: " + str(wins))
    return wins

def GetWinsOld(b, p):
    rnd=[]
    count = 0
    for x in range(len(p)):
        pa = p["ScoreA"][str(x)]  # prediction
        pb = p["ScoreB"][str(x)]
        tpa = p["TeamA"][str(x)]
        tpb = p["TeamB"][str(x)]
        predict = p["Pick"][str(x)]
        print ("predict team: " + tpa + " vs " + tpb)
        print ("predict score: " + str(pa) + " - " + str(pb))
        print ("predict: " + str(predict))
        print (" " )
        idx = p["Index"][str(x)]
        for y in range(len(b)):
            if idx == b[str(y)]["Index"]:
                ba = b[str(y)]["ScoreA"]    # bracket
                bb = b[str(y)]["ScoreB"]
                tba = b[str(y)]["TeamA"]
                tbb = b[str(y)]["TeamB"]
                print ("team: " + tba + " vs " + tbb)
                print ("score: " + ba + " - " + bb)
                print (" ")
                if predict == "TeamA":
                    print (predict)
                    if ba > bb:
                        if tba == tpa:
                            print ("won")
                            count+=1
                        else:
                            print ("teams don't match")
                else:
                    print (predict)
                    if bb > ba:
                        if tbb == tpb:
                            print ("won")
                            count+=1
                        else:
                            print ("teams don't match")
    print ("round: " + str(r) + " won: " + str(count))
    pdb.set_trace()
    return count

def GetWinsOlder(r, b, p):
    count = 0
    for x in range(len(b)):
        if r == b[str(x)]["Round"]:
            ba = b[str(x)]["ScoreA"]    # bracket
            bb = b[str(x)]["ScoreB"]
            tba = b[str(x)]["TeamA"]
            tbb = b[str(x)]["TeamB"]
            print ("team: " + tba + " vs " + tbb)
            print ("score: " + ba + " - " + bb)
            print (" ")
            idx =  b[str(x)]["Index"]
            index=0
            for y in range(len(p)):
                if idx == p["Index"][str(y)]:
                    pa = p["ScoreA"][str(index)]  # prediction
                    pb = p["ScoreB"][str(index)]
                    tpa = p["TeamA"][str(index)]
                    tpb = p["TeamB"][str(index)]
                    predict = p["Pick"][str(index)]
                    print ("predict team: " + tpa + " vs " + tpb)
                    print ("predict score: " + str(pa) + " - " + str(pb))
                    if predict == "TeamA":
                        print (predict)
                        if ba > bb:
                            if tba == tpa:
                                print ("won")
                                count+=1
                            else:
                                print ("teams don't match")
                    else:
                        print (predict)
                        if bb > ba:
                            if tbb == tpb:
                                print ("won")
                                count+=1
                            else:
                                print ("teams don't match")
                    pdb.set_trace()
                index+=1
    
    return count

def GetPercent(t, w):
    if w <= 0:
        return "0%"
    try:
        answer = float(w/t)
    except ValueError:
        return "0%"
    return str("{:.0f}".format(answer*100)) + "%"

year = 0
now = datetime.now()
year = int(now.year)
if (len(sys.argv)>=2):
    year = GetNumber(sys.argv[1])
    if (year < 2002 or year > int(now.year)):
        year = int(now.year)
current_working_directory = os.getcwd()

def main(argv):
    saved_path = "{0}/archive/{1}/".format(current_working_directory, year)
    predict_path = "{0}/".format(current_working_directory)
 
    print ("Measure Actual Results Tool")
    print ("**************************")
    print (" ")
    print ("run this tool after the madness tournament is done")
    print ("        let's see how we did")
    print (" ")
    print ("Year is: {0}".format(year))
    print ("Archive location: {0}".format(saved_path))
    print ("**************************")

    Path(predict_path).mkdir(parents=True, exist_ok=True)
    #RefreshBracket() # turn back on after this tool works

    file = '{0}json/bracket.json'.format(predict_path)
    if (not os.path.exists(file)):
        print ("ncaa bracket is missing, run the scrape_bracket tool to create")
        exit()
    with open(file) as bracket_file:
        bracket_json = json.load(bracket_file, object_pairs_hook=OrderedDict)
    
    Path(predict_path).mkdir(parents=True, exist_ok=True)
    file = '{0}predict.xlsx'.format(predict_path)
    if (not os.path.exists(file)):
        print ("Cannot measure results, no prediction spreadsheet")
        exit()
    excel_df = pd.read_excel(file, sheet_name='Sheet1')
    predict_json = json.loads(excel_df.to_json())

    file = '{0}merge.xlsx'.format(predict_path)
    if (not os.path.exists(file)):
        print ("merge spreadsheet is missing, run the merge_teams tool to create")
        exit() 

    dict_merge={}
    excel_df = pd.read_excel(file, sheet_name='Sheet1')
    dict_merge = json.loads(excel_df.to_json())
    for itm in bracket_json.values():
        teama, teamb = pyMadness.FindMergeTeams(itm["TeamA"], itm["TeamB"], dict_merge)
        itm["TeamA"] = teama
        itm["TeamB"] = teamb
    
    IDX=[]
    ROUND=["First Four", "First Round", "Second Round", "Sweet Sixteen", "Elite Eight", "Final Four", "Championship", "Totals"]
    index = 0
    TOTALS=[]
    WON=[]
    PERCENT=[]
    grand_rnd_count = 0
    wins = GetWins(bracket_json, predict_json)
    for rnd in range(0, 7):
        index+=1
        IDX.append(index)
        rnd_count = GetRoundCount(rnd, bracket_json)
        TOTALS.append(rnd_count)
        grand_rnd_count+=rnd_count
        WON.append(wins[rnd])
        percent = GetPercent(rnd_count, wins[rnd])
        PERCENT.append(percent)
        
    percent = GetPercent(grand_rnd_count, wins[index])
    PERCENT.append(percent)
    WON.append(wins[index])
    index+=1
    IDX.append(index)
    TOTALS.append(grand_rnd_count)
    
    df=pd.DataFrame(IDX,columns=['Index'])
    df['Round']=ROUND
    df['Games']=TOTALS
    df['Won']=WON
    df['Percent']=PERCENT

    print ("... creating results JSON file")
    the_file = "{0}json/results.json".format(saved_path)
    the_path = "{0}json/".format(saved_path)
    Path(the_path).mkdir(parents=True, exist_ok=True)
    with open(the_file, 'w') as f:
        f.write(df.to_json(orient='index'))
    f.close()
    
    print ("... creating results spreadsheet")
    excel_file = "{0}results.xlsx".format(saved_path)
    writer = pd.ExcelWriter(excel_file, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Sheet1", index=False)
    writer.close()
    print ("done.")

if __name__ == "__main__":
    main(sys.argv[1:])
