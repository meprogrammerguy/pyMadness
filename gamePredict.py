#!/usr/bin/env python3
# Data scraped in this way
#  https://gamepredict.us/kenpom?team_a=<first>&team_b=<second>&neutral=<neutral>

from urllib.request import urlopen
from bs4 import BeautifulSoup
import html5lib
import pdb

def predictScore(first, second, neutral, verbose):
    if (neutral):
        wiki = "https://gamepredict.us/kenpom?team_a={0}&team_b={1}&neutral={2}".format(first, second, neutral).lower()
    else:
        wiki = "https://gamepredict.us/kenpom?team_a={0}&team_b={1}".format(first, second).lower()
    if (verbose):
        print (wiki)
    page = urlopen(wiki)
    soup = BeautifulSoup(page, "html5lib")
    scores = soup.findAll("div", {"class": "col-xs-6"})
    line =  soup.findAll("div", {"class": "col-xs-12"})
    #pdb.set_trace() 
    dict_score = {'scorea':scores[5].h3.text, 'chancea':scores[5].p.text.replace("\n", "").strip() ,'scoreb':scores[4].h3.text, 'chanceb':scores[4].p.text.replace("\n", "").strip(), 'line':line[2].text.split()[1].strip(), 'tempo':line[2].findAll('p')[1].text.split()[1] }
    if (verbose):   
        print (dict_score)
    return dict_score
    print (first, second, neutral, verbose)
    dict_score = {'scorea':1, 'chancea':2 ,'scoreb':3, 'chanceb':4, 'line':5, 'tempo':6 }
    return dict_score
