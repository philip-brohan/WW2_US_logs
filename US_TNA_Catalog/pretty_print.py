#!/usr/bin/env python

# Take a single file of TNA catalog, parse the JSON - throw out all the elements
#  I don't need at the moment, and pretty-print the remainder.

import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--filen", help="File name", type=str, required=True)
parser.add_argument(
    "--startl", help="First line to print", type=int, required=False, default=0
)
parser.add_argument(
    "--endl", help="Last line to print", type=int, required=False, default=None
)
args = parser.parse_args()

fd = open(args.filen, "r")
fw = open("reduced", "w")
count = 0
while True:
    line = fd.readline()
    if not line:
        break
    if line[0] == ",":
        continue
    count += 1
    if count < args.startl:
        continue
    if args.endl is not None and count > args.endl:
        break
    if line[:2] == "{[":
        line = line[2:]
    if line[-3:-1] == "]}":
        line = line[:-3] + "\n"
    try:
        fj = json.loads(line)
    except:
        print(line)
        break
    fw.write(json.dumps(fj, indent=4))
