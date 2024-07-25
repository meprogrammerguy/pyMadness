#!/usr/bin/env python3

from urllib.request import urlopen
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
import html5lib
import pdb
import json
import os, sys, stat, time
from collections import OrderedDict
import contextlib
import datetime
import re
from pathlib import Path

def GetNumber(item):
    idx = re.findall(r'\d+', str(item))
    if (len(idx) == 0):
        idx.append("-1")
    return int(idx[0])

def GetSeeds(s, ta, tb, sp):
    ta_seed = s.partition(ta)[0]
    tb_p = s.partition(tb)[0]
    tb_seed = tb_p.split(sp)
    return "{:02d}".format(int(ta_seed)), "{:02d}".format(int(tb_seed[1]))
        
def SetRoundAndRegion(f, s, s16, e8, f4, c, first4):
    rd=[]
    reg=[]    
    for x in range(8):
        rd.append(f)
        reg.append("EAST")
    for x in range(4):
        rd.append(s)
        reg.append("EAST")
    for x in range(2):
        rd.append(s16)
        reg.append("EAST")
    for x in range(1):
        rd.append(e8)
        reg.append("EAST")
       
    for x in range(8):
        rd.append(f)
        reg.append("SOUTH")
    for x in range(4):
        rd.append(s)
        reg.append("SOUTH")
    for x in range(2):
        rd.append(s16)
        reg.append("SOUTH")
    for x in range(1):
        rd.append(e8)
        reg.append("SOUTH")

    for x in range(1):
        rd.append(f4)
        reg.append(" ")

    for x in range(1):
        rd.append(c)
        reg.append(" ")

    for x in range(1):
        rd.append(f4)
        reg.append(" ")

    for x in range(8):
        rd.append(f)
        reg.append("WEST")
    for x in range(4):
        rd.append(s)
        reg.append("WEST")
    for x in range(2):
        rd.append(s16)
        reg.append("WEST")
    for x in range(1):
        rd.append(e8)
        reg.append("WEST")
       
    for x in range(8):
        rd.append(f)
        reg.append("MIDWEST")
    for x in range(4):
        rd.append(s)
        reg.append("MIDWEST")
    for x in range(2):
        rd.append(s16)
        reg.append("MIDWEST")
    for x in range(1):
        rd.append(e8)
        reg.append("MIDWEST")

    for x in range(4):
        rd.append(first4)
        reg.append(" ")
    return rd, reg
    
year = 0
now = datetime.datetime.now()
year = int(now.year)
current_year=True
if (len(sys.argv)>=2):
    year = GetNumber(sys.argv[1])
    current_year=False
    if (year < 2002 or year > int(now.year)):
        year = int(now.year)
        current_year=True
current_working_directory = os.getcwd()

test_mode = False
test_file = "/home/jsmith/git/pyMadness/test/bracket/{0}/ncaa_bracket.html".format(year)
if (os.path.exists(test_file)):
    print("... fetching test bracket page")
    with open(test_file, 'r') as file:
        page = file.read().rstrip()
    soup = BeautifulSoup(page, "html5lib")
    test_mode = True

url = "http://www.ncaa.com/march-madness-live/bracket"

print ("Scrape Bracket Tool")
print ("**************************")
print (" ")
if test_mode:
    print ("*** Test data ***")
    print ("    data is from {0}".format(test_file))
    print ("*** delete test data and re-run to go live ***")
else:
    print ("*** Live ***")
    print ("data is from {0}".format(url))
print (" ")
print ("Year is: {0}".format(year))
print ("data is from {0}".format(url))
print ("**************************")

if not test_mode:
    with contextlib.closing(urlopen(url)) as page:
        soup = BeautifulSoup(page, "html.parser", parse_only=SoupStrainer('a'))
main = soup.find_all('div', attrs = {'class':'bracket-main'})
rows={}
for item in main:
    a_s = item.find_all('a')
    p_s = item.find_all('p')
    index=0
    for row in a_s[3:]:
        idx=0
        COLS=[]
        for i in range(idx*index,len(p_s[3:]),4):
            cols={}
            cols["teama"] = p_s[i+3].text
            cols["scorea"] = p_s[i+4].text
            cols["teamb"] = p_s[i+5].text
            cols["scoreb"] = p_s[i+6].text
            idx+=1
            COLS.append(cols)
        rows[index] = row.text, COLS[index]
        index+=1
IDX=[]
SEEDA=[]
TA=[]
SA=[]
SEEDB=[]
TB=[]
SB=[]
ROUND=[]
REGION=[]
index=0
for row in rows:
    seeda, seedb = GetSeeds(rows[row][0], rows[row][1]["teama"], rows[row][1]["teamb"], rows[row][1]["scorea"])
    SEEDA.append(seeda)
    SEEDB.append(seedb)
    TA.append(rows[row][1]["teama"])
    SA.append(rows[row][1]["scorea"])
    TB.append(rows[row][1]["teamb"])
    SB.append(rows[row][1]["scoreb"])
    index+=1
    IDX.append(index)

ROUND, REGION = SetRoundAndRegion("first", "second", "sweet 16", "elite 8", "final 4", "championship", "first 4")

df=pd.DataFrame(IDX, columns=['Index'])
df['SeedA']=SEEDA
df['TeamA']=TA
df['ScoreA']=SA
df['SeedB']=SEEDB
df['TeamB']=TB
df['ScoreB']=SB
df['Region']=REGION
#df['Venue']=VX
df['Round']=ROUND

print ("... creating bracket JSON file")
the_file = "json/bracket.json"
the_path = "json/"
Path(the_path).mkdir(parents=True, exist_ok=True)
with open(the_file, 'w') as f:
    f.write(df.to_json(orient='index'))
f.close()
    
print ("... creating bracket spreadsheet")
excel_file = "bracket.xlsx"
writer = pd.ExcelWriter(excel_file, engine="xlsxwriter")
df.to_excel(writer, sheet_name="Sheet1", index=False)
writer.close()
print ("done.")

