#!/usr/bin/env python3

import sys, getopt

def main(argv):
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
    print(first)
    print (second)
    print (neutral)

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
