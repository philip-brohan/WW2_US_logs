#!/usr/bin/env python

# Get the catalog IDs of all of the ships in Kevin's spreadsheet
#  and set up the commands to download them.

import csv

with open('complete_list.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print("./download_log.py --id=%s" % row[0])
