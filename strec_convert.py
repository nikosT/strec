#!/usr/bin/env python

from optparse import OptionParser
import sqlite3
import os.path
import sys
import datetime

from strec.mtreader import createDataFile,appendDataFile

usage = """usage: %prog [options] infile outfile
Convert data from CSV, NDK, or QuakeML XML into internal database format (SQLite).
The default input format is CSV.
CSV format columns:
(Required)
1) Date/time (YYYYMMDDHHMMSS or YYYYMMDDHHMM)
2) Lat (dd)
3) Lon (dd)
4) Depth (km)
5) Mag
6) Mrr (dyne-cm)
7) Mtt (dyne-cm)
8) Mpp (dyne-cm)
9) Mrt (dyne-cm)
10) Mrp (dyne-cm)
11) Mtp (dyne-cm)
(Optional - if these are not supplied STREC will calculate them from moment tensor components above).
12) T Azimuth (deg)
13) T Plunge (deg)
14) N Azimuth (deg)
15) N Plunge (deg)
16) P Azimuth (deg)
17) P Plunge (deg)
18) NP1 Strike (deg)
19) NP1 Dip (deg)
20) NP1 Rake (deg)
21) NP2 Strike (deg)
22) NP2 Dip (deg)
23) NP2 Rake (deg)
"""
parser = OptionParser(usage=usage)
parser.add_option("-n", "--ndk",
                  action="store_true", dest="usendk", default=False,
                  help="Input file is in NDK format")
parser.add_option("-x", "--xml",
                  action="store_true", dest="usexml", default=False,
                  help="Input file is in QuakeML XML format")
parser.add_option("-c", "--csv",
                  action="store_true", dest="usecsv", default=False,
                  help="Input file is in CSV format (Default)")
parser.add_option("-s", "--skipfirst",
                  action="store_true", dest="hasheader", default=False,
                  help="CSV file has a header row which should be skipped")
parser.add_option("-t", "--type",dest="fmtype",
                  metavar="TYPE", help="Specify the moment tensor type (cmt,body wave,etc.) Defaults to 'User'.")

(options, args) = parser.parse_args()
if len(args) < 2:
    print 'Missing input and/or output files.'
    parser.print_help()
    sys.exit(0)

suminput = sum([options.usecsv,options.usexml,options.usendk])
    
if suminput > 1:
    print 'You must provide ONLY one of -n, -c, or -x options.'
    parser.print_usage()
    sys.exit(0)

infile = args[0]
outfile = args[1]

if options.fmtype is None:
    options.fmtype = 'User'

if options.usendk:
    filetype = 'ndk'
if options.usecsv:
    filetype = 'csv'
if options.usexml:
    filetype = 'xml'

if os.path.isfile(outfile):
    print '%s already exists - appending new data.' % outfile
    appendDataFile(infile,outfile,filetype,options.fmtype,hasHeader=options.hasheader)
else:
    createDataFile(infile,outfile,filetype,options.fmtype,hasHeader=options.hasheader)
