#!/usr/bin/env python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
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

if current_year:
    url = "http://www.espn.com/mens-college-basketball/tournament/bracket"
else:
    url = "https://www.espn.com/mens-college-basketball/bracket/_/season/{0}".format(year)

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
        soup = BeautifulSoup(page, "html.parser")

IDX=[]
A=[]
B=[]
C=[]
D=[]
E=[]
F=[]
RX=[]
VX=[]
RO=[]
IDX.append(1)
A.append(1)
B.append(2)
C.append(3)
D.append(4)
E.append(5)
F.append(6)
RX.append(7)
VX.append(8)
RO.append(9)

df=pd.DataFrame(IDX, columns=['Index'])
df['SeedA']=A
df['TeamA']=B
df['ScoreA']=C
df['SeedB']=D
df['TeamB']=E
df['ScoreB']=F
df['Region']=RX
df['Venue']=VX
df['Round']=RO

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

