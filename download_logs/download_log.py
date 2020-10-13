#!/usr/bin/env python

# Download one of Kevin's logs (as a set of JPGs)
#  given its catalogue number.

import urllib.request
import json
import os

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--id", help="NARA catalogue ID", type=int, required=True)
args = parser.parse_args()

# Get the catalogue entry
catalogue = json.loads(
    urllib.request.urlopen("https://catalog.archives.gov/api/v1/?naIds=%d" % args.id)
    .read()
    .decode("utf-8")
)

print("Started %d" % args.id)

# List of documents
docs = catalogue["opaResponse"]["results"]["result"][0]["objects"]["object"]

for doc in docs:
    a_url = doc["file"]["@url"]
    ftype = a_url[-3:].lower()
    if ftype == "jpg":
        fname = os.path.basename(a_url)
        fyr = fname[-7:-3]
        fmo = fname[-2:]
        ldir = os.path.basename(os.path.dirname(a_url))
        fyr = ldir[-7:-3]
        fmo = ldir[-2:]
        ldir = "%s/WW2_US_logs/%s/%s/%s" % (os.getenv("SCRATCH"), fyr, fmo, ldir)
        if not os.path.exists(ldir):
            os.makedirs(ldir)
        # Already got?
        if os.path.isfile("%s/%s" % (ldir, fname)):
            continue
        # Download a_url to ldir/fname
        urllib.request.urlretrieve(a_url, "%s/%s" % (ldir, fname))

print("%d OK" % args.id)
