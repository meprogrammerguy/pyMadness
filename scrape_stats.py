#!/usr/bin/env python3

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import html5lib
import pdb
from collections import OrderedDict
import json
import contextlib
import os.path
from pathlib import Path

url = "https://kenpom.com/index.php"

#url = "https://kenpom.com/index.php?y=2017" #past year testing override

print ("Scrape Statistics Tool")
print ("**************************")
print ("data is from {0}".format(url))
print ("**************************")

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with contextlib.closing(urlopen(req)) as page:
    soup = BeautifulSoup(page, "html5lib")
ratings_table=soup.find('table', id='ratings-table')

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
L=[]
M=[]
index=0
for row in ratings_table.findAll("tr"):
    col=row.findAll('td')
    if len(col)>0:
        index+=1
        IDX.append(index)
        A.append(col[0].find(string=True))
        B.append(col[1].find(string=True))
        C.append(col[2].find(string=True))
        D.append(col[3].find(string=True))
        E.append(col[4].find(string=True))
        F.append(col[5].find(string=True))
        G.append(col[7].find(string=True))
        H.append(col[9].find(string=True))
        I.append(col[11].find(string=True))
        J.append(col[13].find(string=True))
        K.append(col[15].find(string=True))
        L.append(col[17].find(string=True))
        M.append(col[19].find(string=True))

df=pd.DataFrame(IDX,columns=['Index'])
df['Rank']=A
df['Team']=B
df['Conf']=C
df['W-L']=D
df['AdjEM']=E
df['AdjO']=F
df['AdjD']=G
df['AdjT']=H
df['Luck']=I
df['AdjEMSOS']=J
df['OppOSOS']=K
df['OppDSOS']=L
df['AdjEMNCSOS']=M

print ("... creating stats JSON file")
the_file = "json/stats.json"
the_path = "json/"
Path(the_path).mkdir(parents=True, exist_ok=True)
with open(the_file, 'w') as f:
    f.write(df.to_json(orient='index'))
f.close()
    
print ("... creating stats spreadsheet")
excel_file = "stats.xlsx"
writer = pd.ExcelWriter(excel_file, engine="xlsxwriter")
df.to_excel(writer, sheet_name="Sheet1", index=False)
writer.close()
print ("done.")
