#!/usr/bin/env python

# Make a csv file, that matches Kevin's spreadsheet, from the TNA Archive dump

import os
import sys
import json
import argparse
from calendar import monthrange

parser = argparse.ArgumentParser()
parser.add_argument("--rg", help="Record group", type=int, required=True)
parser.add_argument(
    "--subgroup", help="Record group file", type=int, required=False, default=None
)
parser.add_argument("--series", help="Series", type=int, required=True)
parser.add_argument("--match", help="Filter", type=str, required=False, default=None)
parser.add_argument("--title", default=False, action="store_true")
args = parser.parse_args()

# Write to stdout
fw = sys.stdout

# Input files
fileN = []
filed = "%s/WW2_US_logs/US_TNA_Catalog/record-groups/rg_%03d/" % (
    os.getenv("SCRATCH"),
    args.rg,
)
if args.subgroup is not None:
    fileN.append("%s/rg_%03d-%03d.json" % (filed, args.rg, args.subgroup))
else:
    files = os.listdir(filed)
    for fn in files:
        fileN.append("%s/%s" % (filed, fn))

# Get the date (month) from the title, where posible
mnames = (
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
)


def getMonthFromTitle(title):
    hIdx = title.rfind("-")
    title = title[hIdx:].lower()
    # year is the last 4 characters
    year = int(title[-4:])
    # which month matches
    mmatch = -1
    for count in range(len(mnames)):
        if title.find(mnames[count]) > -1:
            mmatch = count + 1
            break
    if mmatch < 1:
        raise Exception("Month not found")
    return [year, mmatch]


# Get the date at the end of the valid month
def getEndDate(record):
    try:
        (year, month) = getMonthFromTitle(record["title"])
        return [year, month, monthrange(year, month)[1]]
    except Exception:
        ed = record["coverageDates"]["coverageEndDate"]
        if "logicalDate" in ed:
            return (
                int(ed["logicalDate"][:4]),
                int(ed["logicalDate"][5:7]),
                int(ed["logicalDate"][8:10]),
            )
        else:
            return (
                int(ed["year"]),
                int(ed["month"]),
                monthrange(int(ed["year"]), int(ed["month"]))[1],
            )


# Add the column titles if requested
if args.title:
    fw.write(
        "Ship Name, Hull Symbol, Record Group, Series NAID, Record Entry, Container, "
        + "StartDate, EndDate, Nara URL, #Images, Document URL\n"
    )


for filen in fileN:
    fd = open(filen, "r")
    while True:
        line = fd.readline()
        if not line:
            break
        if line[0] == ",":
            continue
        if args.match is not None and args.match not in line:
            continue
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
            if int(base["parentSeries"]["naId"]) != args.series:
                continue
        except Exception:
            continue

        # Name is the portion of the title before the parentheses
        try:
            shipName = base["title"]
            pIdx = base["title"].find("(")
            if pIdx > 0:
                shipName = base["title"][: (pIdx - 1)]
            fw.write('"%-30s",' % shipName)
        except Exception:
            fw.write("%-30s," % " ")

        # Hull number is the portion of the title between parentheses
        try:
            hullNo = ""
            pIdx1 = base["title"].find("(")
            pIdx2 = base["title"].find(")")
            if pIdx1 > 0 and pIdx2 > pIdx1:
                hullNo = base["title"][(pIdx1 + 1) : (pIdx2)]
            fw.write('"%-10s",' % hullNo)
        except Exception:
            fw.write("%-10s," % " ")

        # Fixed data - record group and parent series
        fw.write("%-5d," % args.rg)
        fw.write("%-8d," % args.series)

        # Record entry?
        try:
            vcn = base["variantControlNumberArray"]["variantControlNumber"]
            for entry in vcn:
                if entry["type"]["naId"] == "10675882":
                    fw.write("%-10s," % entry["number"])
                    break
        except Exception as e:
            # sys.stderr.write(repr(e))
            fw.write("%-10s," % " ")

        # Container
        try:
            pFile = base["physicalOccurrenceArray"]["fileUnitPhysicalOccurrence"]
            cid = pFile["mediaOccurrenceArray"]["mediaOccurrence"]["containerId"]
            fw.write("%-5s," % cid)
        except Exception as e:
            # sys.stderr.write(repr(e))
            fw.write("%-5s," % " ")

        # dates
        try:
            ed = getEndDate(base)
            fw.write("%04d-%02d-%02d," % (ed[0], ed[1], 1))
            fw.write("%04d-%02d-%02d," % (ed[0], ed[1], ed[2]))
        except Exception as e:
            fw.write("%10s,%10s," % (" ", " "))

        # Nara URL
        try:
            fw.write("https://catalog.archives.gov/id/%s," % base["naId"])
        except Exception:
            fw.write("%-40s," % " ")

        # Count of images
        try:
            nImages = len(fj["objects"]["object"]) - 1  # Don't count the pdf
            fw.write("%-5d," % nImages)
        except Exception as e:
            # sys.stderr.write(repr(e))
            fw.write("%-5s," % " ")

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
    fd.close()
