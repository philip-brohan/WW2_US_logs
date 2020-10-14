#!/usr/bin/env python

# Archive downloaded 20CRv3 data in MASS

import sys
import os
import subprocess
import glob

# What to store
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year", type=int, required=True)
parser.add_argument("--month", help="Integer month", type=int, required=True)
args = parser.parse_args()

# MASS directory
mdir = "moose:/adhoc/projects/20cr/document_images/ships/WW2_US_logs"

# Disc data dir
ddir = "%s/WW2_US_logs" % (os.environ["SCRATCH"])

# Don't overwrite if alerady archived
proc = subprocess.Popen(
    "moo test -f %s/%04d%02d.tar" % (mdir, args.year, args.month),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True,
)
(out, err) = proc.communicate()
if len(err) != 0:
    print(err)
    raise Exception("Failed to check MASS - is it working?")
if out == b"true\n":
    raise Exception("Already archived")

# Are there any logbooks to archive?
ofiles = glob.glob("%s/%04d/%02d/*" % (ddir, args.year, args.month))
if len(ofiles) == 0:  # No logbooks on disc
    raise Exception("No logbooks on disc for %04d-%02d" % (args.year, args.month))

# Pack the month's logbooks into a single file
otarf = "%s/%04d%02d.tar" % (ddir, args.year, args.month)
proc = subprocess.Popen(
    "cd %s ; tar cf %s %04d/%02d" % (ddir, otarf, args.year, args.month),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True,
)
(out, err) = proc.communicate()
if len(err) != 0:
    print(err)
    raise Exception("Failed to tar logbooks")

proc = subprocess.Popen(
    "moo put %s %s" % (otarf, mdir),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True,
)
(out, err) = proc.communicate()
if len(err) != 0:
    print(err)
    raise Exception("Failed to write to MASS - is it working?")

# Clean up
os.remove(otarf)
