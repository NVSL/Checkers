#!/usr/bin/env python


import argparse
import os

import ProChecker

def main():
    parser = argparse.ArgumentParser(description="Returns 0 if pro is at 100%, -1 otherwise.")
    parser.add_argument("filename", type=str, nargs=1, help="The pro file to check")
    args = parser.parse_args()
    args.filename = args.filename[0]   

    if not os.path.exists(args.filename):
        raise IOError("Could not find file: "+args.filename)

    file = open(args.filename)
    percent = ProChecker.check_routing_percent(file.read())
    print "Autorouting completed: "+str(percent)+"%"

    if percent == 100.0:
        exit(0)
    else:
        exit(-1)

if __name__ == "__main__":
    main()
