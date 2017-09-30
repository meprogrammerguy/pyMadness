#!/usr/bin/env python3
#
# Data scraped in this way
#  https://gamepredict.us/kenpom?team_a=<first>&team_b=<second>&neutral=<neutral>
#
import sys, getopt
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import html5lib
import pdb

def main(argv):
    wiki = ""
    first = ""
    second = ""
    verbose = False
    neutral = False
    try:
        opts, args = getopt.getopt(argv, "hf:s:vn", ["help", "first=", "second=", "verbose", "neutral"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o in ("-v", "--verbose"):
            verbose = True
        elif o in ("-n", "--neutral"):
            neutral = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-f", "--first"):
            first = a
        elif o in ("-s", "--second"):
            second = a
        else:
            assert False, "unhandled option"
    wiki = "https://gamepredict.us/kenpom?team_a={0}&team_b={1}&neutral={2}".format(first, second, neutral)
    page = urlopen(wiki)
    soup = BeautifulSoup(page, "html5lib")
    scores = soup.findAll("div", {"class": "col-xs-6"})
    line =  soup.findAll("div", {"class": "col-xs-12"})
    pdb.set_trace()
    # print (scores[4].h3.text)
    # print (scores[4].p.text)
    # print (scores[5].h3.text)
    # print (scores[5].p.text)
    # print (line[2])
def usage():
    usage = """
    -h --help                 Prints this
    -v --verbose              Increases the information level
    -f --first                First Team (The Away Team)
    -s --second               Second Team (The Home Team)
    -n --neutral              Playing on a neutral Field
    """
    print (usage)

if __name__ == "__main__":
  main(sys.argv[1:])
