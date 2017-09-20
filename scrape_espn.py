#!/usr/bin/env python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import html5lib
import pdb

wiki = "http://www.espn.com/mens-college-basketball/tournament/bracket"
page = urlopen(wiki)
soup = BeautifulSoup(page, "html5lib")

IDX=[]
A=[]
B=[]
C=[]
D=[]
E=[]
F=[]
index = 0
for row in soup.findAll("dl"):
    index+=1
    info=row.findAll(text=True)
    #pdb.set_trace()
    IDX.append(index)
    A.append(info[0])
    B.append(info[1])
    C.append(info[4])
    D.append(info[2])
    E.append(info[3])
    F.append(info[5])
df=pd.DataFrame(IDX, columns=['Index'])
df['SeedA']=A
df['TeamA']=B
df['ScoreA']=C
df['SeedB']=D
df['TeamB']=E
df['ScoreB']=F
with open('espn.json', 'w') as f:
    f.write(df.to_json(orient='index'))
