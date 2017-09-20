#!/usr/bin/env python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import html5lib

wiki = "http://www.espn.com/mens-college-basketball/tournament/bracket"
page = urlopen(wiki)
soup = BeautifulSoup(page, "html5lib")

A=[]
B=[]
C=[]
D=[]
E=[]
F=[]
for row in soup.findAll("dl"):
    team=row.findAll('a')
    info=row.findAll(text=True)
    A.append(info[0])
    B.append(team[0].find(text=True))
    C.append(info[4])
    D.append(info[2])
    E.append(team[1].find(text=True))
    F.append(info[5])
df=pd.DataFrame(A,columns=['SeedA'])
df['TeamA']=B
df['ScoreA']=C
df['SeedB']=D
df['TeamB']=E
df['ScoreB']=F
with open('espn.json', 'w') as f:
    f.write(df.to_json(orient='records', lines=True))
