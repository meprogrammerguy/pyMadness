#!/usr/bin/env python3
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import html5lib
import pdb

wiki = "http://www.espn.com/mens-college-basketball/tournament/bracket"
page = urlopen(wiki)
soup = BeautifulSoup(page, "html5lib")

region = soup.findAll("div", {"class": "regtitle"})
R=[]
for row in region:
    R.append(row.find(text=True))
#pdb.set_trace()

venue1 = soup.findAll("div", {"class": "venue v1"})
V1=[]
for row in venue1:
    V1.append(row.find(text=True))

venue2 = soup.findAll("div", {"class": "venue v2"})
V2=[]
for row in venue2:
    V2.append(row.find(text=True))
#pdb.set_trace()

IDX=[]
A=[]
B=[]
C=[]
D=[]
E=[]
F=[]
RX=[]
VX=[]
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
    if (index == 1):
        RX.append(R[3]) #South
    elif (index in range(2, 4)):
        RX.append(R[0]) #East
    elif (index == 4):
        RX.append(R[2]) #Midwest
    else :
        RX.append("?")
    VX.append("?")

df=pd.DataFrame(IDX, columns=['Index'])
df['SeedA']=A
df['TeamA']=B
df['ScoreA']=C
df['SeedB']=D
df['TeamB']=E
df['ScoreB']=F
df['Region']=RX
df['Venue']=VX

with open('espn.json', 'w') as f:
    f.write(df.to_json(orient='index'))
