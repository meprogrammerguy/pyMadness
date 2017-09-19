#!/usr/bin/env python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

wiki = "http://www.ncaa.com/interactive-bracket/basketball-men/d1"
page = urlopen(wiki)
soup = BeautifulSoup(page, "lxml")
sections=soup.find_all('div class=team-name')
print (sections)
#with open('ncaa.json', 'w') as f:
#    f.write(df.to_json(orient='records', lines=True))
