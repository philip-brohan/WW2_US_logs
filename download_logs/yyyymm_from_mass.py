#!/usr/bin/env python

# Retrieve archived WW2 US logbook images (Kevin's) from MASS

import sys
import os
import subprocess
import os.path
import glob
import re

# What to store
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year", type=int, required=True)
parser.add_argument("--month", help="Integer month", type=int, required=True)
args = parser.parse_args()

# Base location for storage
mdir = "moose:/adhoc/projects/20cr/document_images/ships/WW2_US_logs"

# Disc data dir
ddir = "%s/WW2_US_logs/" % os.environ["SCRATCH"]
if not os.path.isdir(ddir):
    os.makedirs(ddir)

ofiles = glob.glob("%s/%04d/%02d/*" % (ddir, args.year, args.month))
if len(ofiles) > 0:
    raise Exception("Already images on disc")

proc = subprocess.Popen(
    "moo ls %s/%04d%02d.tar" % (mdir, args.year, args.month),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True,
)
(out, err) = proc.communicate()
if len(err) != 0:
    raise Exception("No images on mass")

proc = subprocess.Popen(
    "moo get %s/%04d%02d.tar %s" % (mdir, args.year, args.month, ddir),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True,
)
(out, err) = proc.communicate()
if len(err) != 0:
    print(err)
    raise Exception("Failed to retrieve images from MASS")

otarf = "%s/%04d%02d.tar" % (ddir, args.year, args.month)
proc = subprocess.Popen(
    "cd %s ; tar xf %s" % (ddir, otarf),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True,
)
(out, err) = proc.communicate()
if len(err) != 0:
    print(err)
    raise Exception("Failed to untar logbooks")

# Reset the modification time -
#     otherwise scratch will delete them.
members = glob.glob("%s/%04d/%02d/*/*" % (ddir, args.year, args.month))
for member in members:
    os.utime(member, None)

# Clean up
os.remove(otarf)
