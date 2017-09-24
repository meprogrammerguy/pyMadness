#!/usr/bin/env python3

import sys, getopt

def main(argv):
    first = ""
    second = ""
    verbose = False
    try:
        opts, args = getopt.getopt(argv, "hf:s:v", ["help", "first=", "second="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
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

def usage():
    usage = """
    -h --help                 Prints this
    -v --verbose              Increases the information level
    -f --first                First Team
    -s --second               Second Team
    """
    print (usage)

if __name__ == "__main__":
  main(sys.argv[1:])
