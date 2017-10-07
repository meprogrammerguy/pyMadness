#!/usr/bin/env python3
from urllib.request import urlopen
from bs4 import BeautifulSoup
import html5lib
import pdb

def predictScore(first, second, neutral, verbose):
    if (verbose):
        if (neutral):
            info = "{0} verses {1} at a neutral location".format(first, second)
            print (info)
        else:
            print (first, second, neutral, verbose)

    dict_score = {'scorea':1, 'chancea':2 ,'scoreb':3, 'chanceb':4, 'line':5, 'tempo':6 }
    return dict_score
