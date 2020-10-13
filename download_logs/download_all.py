#!/usr/bin/env python

# Get the catalog IDs of all of the ships in Kevin's spreadsheet
#  and set up the commands to download them.

import csv

# Get lists of catalog ID and yyyy-mm
ids = []
yyyymm = []
with open("complete_list.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        ids.append(row[0])
        yyyymm.append(row[5][-7:])

# Get catalogue ids in ascending date order
ids2 = [x for _, x in sorted(zip(yyyymm, ids))]
for id in ids2:
    print("./download_log.py --id=%s" % id)
