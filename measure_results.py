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

def GetWins(r, b, p):
    return 1

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
 
    IDX=[]
    ROUND=["First Four", "First Round", "Second Round", "Sweet Sixteen", "Elite Eight", "Final Four", "Championship"]
    index = 0
    TOTALS=[]
    WON=[]
    PERCENT=[]
    grand_rnd_count = 0
    grand_wins=0
    for rnd in range(0, 7):
        index+=1
        IDX.append(index)
        rnd_count = GetRoundCount(rnd, bracket_json)
        wins = GetWins(rnd, bracket_json, predict_json)
        WON.append(wins)
        grand_wins+=wins
        TOTALS.append(rnd_count)
        grand_rnd_count+=rnd_count
        percent = GetPercent(rnd_count, wins)
        PERCENT.append(percent)
        
    ROUND.append("Totals")             #grand totals row
    index+=1
    IDX.append(index)
    TOTALS.append(grand_rnd_count)
    WON.append(grand_wins)
    percent = GetPercent(grand_rnd_count, grand_wins)
    PERCENT.append(percent)
    
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
