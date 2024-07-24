#!/usr/bin/env python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import html5lib
import pdb
import json
import csv
from collections import OrderedDict
import contextlib

url = "http://www.espn.com/mens-college-basketball/tournament/bracket"

print ("Scrape Bracket Tool")
print ("**************************")
print ("data is from {0}".format(url))
print ("**************************")

with contextlib.closing(urlopen(url)) as page:
    soup = BeautifulSoup(page, "html.parser")
region = soup.findAll("script", {"type": "text/javascript"})
R=[]
for row in region:
    R.append(row.find(text=True))
venue1 = soup.findAll("div", {"class": "venue v1"})
V1=[]
for row in venue1:
    V1.append(row.find(text=True))
venue2 = soup.findAll("div", {"class": "venue v2"})
V2=[]
for row in venue2:
    V2.append(row.find(text=True))
venue3 = soup.findAll("div", {"class": "venue v3"})
V3=[]
for row in venue3:
    V3.append(row.find(text=True))
venue4 = soup.findAll("div", {"class": "venue v4"})
V4=[]
for row in venue4:
    V4.append(row.find(text=True))
venue5 = soup.findAll("div", {"class": "venue v5"})
V5=[]
for row in venue5:
    V5.append(row.find(text=True))
venuef = soup.findAll("div", {"class": "venue final"})
VF=[]
for row in venuef:
    VF.append(row.find(text=True))

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
index = 0
for row in soup.findAll("dl"):
    index+=1
    info=row.findAll(text=True)
    IDX.append(index)
    if (not info):
        A.append("?")
        B.append("?")
        C.append("?")
        D.append("?")
        E.append("?")
        F.append("?")
    else:
        if len(info) > 0:
            A.append(info[0])
        else:
            A.append("?")
        if len(info) > 1:
            B.append(info[1])
        else:
            B.append("?")
        C.append("?")
        if len(info) > 2:
            D.append(info[2])
        else:
            D.append("?")
        if len(info) > 3:
            E.append(info[3])
        else:
            E.append("?")
        F.append("?")
    if (index in range(1, 5)):
        RX.append("First Four")
        RO.append(0)
        VX.append("Dayton, OH")
    elif (index in range(5, 13)):
        RX.append(R[0]) #East
        RO.append(1)
    elif (index in range(13, 17)):
        RX.append(R[0]) #East
        RO.append(2)
    elif (index in range(17, 19)):
        RX.append(R[0]) #East
        RO.append(3)
    elif (index == 19):
        RX.append(R[0]) #East
        RO.append(4)
    elif (index in range(20, 28)):
        RX.append(R[1]) #West
        RO.append(1)
    elif (index in range(28, 32)):
        RX.append(R[1]) #West
        RO.append(2)
    elif (index in range(32, 34)):
        RX.append(R[1]) #West
        RO.append(3)
    elif (index == 34):
        RX.append(R[1]) #West
        RO.append(4)
    elif (index in range(35, 43)):
        RX.append(R[2]) #Midwest
        RO.append(1)
    elif (index in range(43, 47)):
        RX.append(R[2]) #Midwest
        RO.append(2)
    elif (index in range(47, 49)):
        RX.append(R[2]) #Midwest
        RO.append(3)
    elif (index == 49):
        RX.append(R[2]) #Midwest
        RO.append(4)
    elif (index in range(50, 58)):
        RX.append(R[3]) #South
        RO.append(1)
    elif (index in range(58, 62)):
        RX.append(R[3]) #South
        RO.append(2)
    elif (index in range(62, 64)):
        RX.append(R[3]) #South
        RO.append(3)
    elif (index == 64):
        RX.append(R[3]) #South
        RO.append(4)
    elif (index in range(65, 67)):
        RX.append("Final Four")
        RO.append(5)
    elif (index == 67):
        RX.append("Championship") 
        RO.append(6)
    else :
        RX.append("?")
        RO.append("?")
    if (index in range(5, 7) or index == 13):
        VX.append(V1[0])
    elif (index in range(20, 22) or index == 28):
        VX.append(V1[1])
    elif (index in range(35, 37) or index == 43):
        VX.append(V1[2])
    elif (index in range(50, 52) or index == 58):
        VX.append(V1[3])
    elif (index in range(7, 9) or index == 14):
        VX.append(V2[0])
    elif (index in range(22, 24) or index == 29):
        VX.append(V2[1])
    elif (index in range(37, 39) or index == 44):
        VX.append(V2[2])
    elif (index in range(52, 54) or index == 59):
        VX.append(V2[3])
    elif (index in range(9, 11) or index == 15):
        VX.append(V3[0])
    elif (index in range(24, 26) or index == 30):
        VX.append(V3[1])
    elif (index in range(39, 41) or index == 45):
        VX.append(V3[2])
    elif (index in range(54, 56) or index == 60):
        VX.append(V3[3])
    elif (index in range(11, 13) or index == 16):
        VX.append(V4[0])
    elif (index in range(26, 28) or index == 31):
        VX.append(V4[1])
    elif (index in range(41, 43) or index == 46):
        VX.append(V4[2])
    elif (index in range(56, 58) or index == 61):
        VX.append(V4[3])
    elif (index in range(17, 19) or index == 19):
        VX.append(V5[0])
    elif (index in range(32, 34) or index == 34):
        VX.append(V5[1])
    elif (index in range(47, 49) or index == 49):
        VX.append(V5[2])
    elif (index in range(62, 64) or index == 64):
        VX.append(V5[3])
    elif (index in range(65, 68)):
        VX.append(VF[0])

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

with open('bracket.json', 'w') as f:
    f.write(df.to_json(orient='index'))

with open("bracket.json") as bracket_json:
    dict_bracket = json.load(bracket_json, object_pairs_hook=OrderedDict)
bracket_sheet = open('bracket.csv', 'w', newline='')
csvwriter = csv.writer(bracket_sheet)
count = 0
for row in dict_bracket.values():
    if (count == 0):
        header = row.keys()
        csvwriter.writerow(header)
        count += 1
    csvwriter.writerow(row.values())
bracket_sheet.close()
print ("done.")
