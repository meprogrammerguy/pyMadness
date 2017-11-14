#!/usr/bin/env python3

from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
import html5lib
import pdb
import contextlib

def Score(first, second, neutral, verbose):
    if (neutral):
        url = "https://gamepredict.us/kenpom?team_a={0}&team_b={1}&neutral=true".format(quote(first), quote(second))
    else:
        url = "https://gamepredict.us/kenpom?team_a={0}&team_b={1}".format(quote(first), quote(second))
    if (verbose):
        print (url)
    with contextlib.closing(urlopen(url)) as page:
        soup = BeautifulSoup(page, "html5lib")
    scores = soup.findAll("div", {"class": "col-xs-6"})
    line =  soup.findAll("div", {"class": "col-xs-12"})
    dict_score = {'teama':first, 'scorea':scores[4].h3.text, 'chancea':scores[4].p.text.replace("\n", "").strip() ,'teamb':second, 'scoreb':scores[5].h3.text, 'chanceb':scores[5].p.text.replace("\n", "").strip(), 'line':line[2].text.split()[1].strip(), 'tempo':line[2].findAll('p')[1].text.split()[1] }
    if (verbose):   
        print (dict_score)
    return dict_score
