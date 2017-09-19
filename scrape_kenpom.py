#!/usr/bin/env python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

wiki = "https://kenpom.com/"
page = urlopen(wiki)
soup = BeautifulSoup(page, "html.parser")
ratings_table=soup.find('table', id='ratings-table')
A=[]
B=[]
C=[]
D=[]
E=[]
F=[]
G=[]
for row in ratings_table.findAll("tr"):
    col=row.findAll('td')
    #import pdb; pdb.set_trace()
    if len(col)>0:
        A.append(col[0].find(text=True))
        B.append(col[1].find(text=True))
        C.append(col[2].find(text=True))
        D.append(col[3].find(text=True))
        E.append(col[4].find(text=True))
        F.append(col[5].find(text=True))
        G.append(col[7].find(text=True))

df=pd.DataFrame(A,columns=['Rank'])
df['Team']=B
df['Conf']=C
df['W-L']=D
df['AdjEM']=E
df['AdjO']=F
df['AdjD']=G
print (df)
with open('kenpom.json', 'w') as f:
    f.write(df.to_json(orient='records', lines=True))
