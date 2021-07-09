#!/usr/bin/env python

# Take a single file of TNA catalog, parse the JSON and print a selected subset.

import sys
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
# fw = open("selected", "w")
fw = sys.stdout
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
    try:
        base = fj["description"]["fileUnit"]
    except Exception:
        continue
    try:
        if base["parentSeries"]["naId"] != "594258":
            continue
    except Exception:
        continue

    try:
        fw.write('"%-50s",' % base["title"])
    except Exception:
        fw.write("%-50s," % " ")
    try:
        fw.write("%10s," % base["naId"])
    except Exception:
        fw.write("%10s," % " ")
    try:
        sd = base["coverageDates"]["coverageStartDate"]
        if "logicalDate" in sd:
            fw.write("%10s," % sd["logicalDate"][:10])
        elif "year" in sd:
            ld = "%4s" % sd["year"]
            if "month" in sd:
                ld += "-%02d" % int(sd["month"])
                if "day" in sd:
                    ld += "-%02d" % int(sd["day"])
            fw.write("%10s," % ld)
        else:
            fw.write("%10s," % " ")
    except Exception:
        fw.write("%10s," % " ")
    try:
        ed = base["coverageDates"]["coverageEndDate"]
        if "logicalDate" in ed:
            fw.write("%10s," % ed["logicalDate"][:10])
        elif "year" in ed:
            ld = "%4s" % ed["year"]
            if "month" in ed:
                ld += "-%02d" % int(ed["month"])
                if "day" in ed:
                    ld += "-%02d" % int(ed["day"])
            fw.write("%10s," % ld)
        else:
            fw.write("%10s," % " ")
    except Exception:
        fw.write("%10s," % " ")
    #    try:
    #        fw.write("%10s," % base['specificRecordsTypeArray']['specificRecordsType']['naId'])
    #    except Exception:
    #        fw.write("%10s," % " ")
    # Get the pdf url, if there is one
    try:
        docs = fj["objects"]["object"]
        pdfU = None
        for doc in docs:
            a_url = doc["file"]["@url"]
            ftype = a_url[-3:].lower()
            if ftype == "pdf":
                pdfU = a_url
                break
        if pdfU is not None:
            fw.write("%s," % pdfU)
        else:
            fw.write("%10s," % " ")
    except Exception:
        fw.write("%10s," % " ")
    fw.write("\n")
