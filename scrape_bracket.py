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
        
def SetNextSlot():
    slots=[]
    slots.append(1)     # EAST
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
        
    slots.append(1)     # SOUTH
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    
    slots.append(1)     # Final Four
    slots.append(0)     # Championship
    slots.append(2)     # Final Four

    slots.append(1)     # WEST
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(2)
        
    slots.append(1)     # MIDWEST
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(1)
    slots.append(2)
    slots.append(2)
    
    slots.append(2)     # First Four
    slots.append(2)
    slots.append(2)
    slots.append(2)
    return slots
    
def SetNextMatch():
    mch=[]
    for x in range(2):      # EAST
        mch.append(9)
    for x in range(2):
        mch.append(10)
    for x in range(2):
        mch.append(11)
    for x in range(2):
        mch.append(12)
    for x in range(2):
        mch.append(13)
    for x in range(2):
        mch.append(14)
    for x in range(2):
        mch.append(15)
    mch.append(31)
        
    for x in range(2):      # SOUTH
        mch.append(24)
    for x in range(2):
        mch.append(25)
    for x in range(2):
        mch.append(26)
    for x in range(2):
        mch.append(27)
    for x in range(2):
        mch.append(28)
    for x in range(2):
        mch.append(29)
    for x in range(2):
        mch.append(30)
    mch.append(33)
    
    mch.append(32)          # Final Four
    
    mch.append(0)           # Championship

    mch.append(32)          # Final Four 

    for x in range(2):      # WEST
        mch.append(42)
    for x in range(2):
        mch.append(43)
    for x in range(2):
        mch.append(44)
    for x in range(2):
        mch.append(45)
    for x in range(2):
        mch.append(46)
    for x in range(2):
        mch.append(47)
    for x in range(2):
        mch.append(48)
    mch.append(31)    

    for x in range(2):      # MIDWEST
        mch.append(57)
    for x in range(2):
        mch.append(58)
    for x in range(2):
        mch.append(59)
    for x in range(2):
        mch.append(60)
    for x in range(2):
        mch.append(61)
    for x in range(2):
        mch.append(62)
    for x in range(2):
        mch.append(63)
    mch.append(33)    

    mch.append(34)          # First Four
    mch.append(55)    
    mch.append(49)    
    mch.append(22)  
    return mch
    
def SetRoundRegion():
    rd=[]
    reg=[]
    for x in range(8):
        rd.append(1)
        reg.append("EAST")
    for x in range(4):
        rd.append(2)
        reg.append("EAST")
    for x in range(2):
        rd.append(3)
        reg.append("EAST")
    for x in range(1):
        rd.append(4)
        reg.append("EAST")

    for x in range(8):
        rd.append(1)
        reg.append("SOUTH")
    for x in range(4):
        rd.append(2)
        reg.append("SOUTH")
    for x in range(2):
        rd.append(3)
        reg.append("SOUTH")
    for x in range(1):
        rd.append(4)
        reg.append("SOUTH")

    for x in range(1):
        rd.append(5)
        reg.append("Final Four")

    for x in range(1):
        rd.append(6)
        reg.append("Championship")

    for x in range(1):
        rd.append(5)
        reg.append("Final Four")

    for x in range(8):
        rd.append(1)
        reg.append("WEST")
    for x in range(4):
        rd.append(2)
        reg.append("WEST")
    for x in range(2):
        rd.append(3)
        reg.append("WEST")
    for x in range(1):
        rd.append(4)
        reg.append("WEST")
       
    for x in range(8):
        rd.append(1)
        reg.append("MIDWEST")
    for x in range(4):
        rd.append(2)
        reg.append("MIDWEST")
    for x in range(2):
        rd.append(3)
        reg.append("MIDWEST")
    for x in range(1):
        rd.append(4)
        reg.append("MIDWEST")

    for x in range(4):
        rd.append(0)
        reg.append("First Four")
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
test_file = "/home/jsmith/git/pyMadness/test/bracket/{0}/bracket.html".format(year)
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
    print ("*** delete test data and re-run to go live ***")
    print (" ")
    print ("    data is from {0}".format(test_file))
else:
    print ("*** Live ***")
    print ("data is from {0}".format(url))
print (" ")
print ("Year is: {0}".format(year))
print ("**************************")

if not test_mode:
    with contextlib.closing(urlopen(url)) as page:
        soup = BeautifulSoup(page, "html5lib")

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
NEXTMATCH=[]
NEXTSLOT=[]
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

ROUND, REGION = SetRoundRegion()
NEXTMATCH = SetNextMatch()
NEXTSLOT = SetNextSlot()

df=pd.DataFrame(IDX, columns=['Index'])
df['SeedA']=SEEDA
df['TeamA']=TA
df['ScoreA']=SA
df['SeedB']=SEEDB
df['TeamB']=TB
df['ScoreB']=SB
df['Region']=REGION
df['Round']=ROUND
df['Next Match']=NEXTMATCH
df['Next Slot']=NEXTSLOT

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

