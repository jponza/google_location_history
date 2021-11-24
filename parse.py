#!/usr/bin/env python

"""
    This script will parse a set of Google's 'Semantic Location Hisory' exports (from Timeline).
    It will normalize and format them into a CSV with lines containing a 'visit' each, and
    having the following fields:

        placeID, placeName, placeLocation, latitude, longitude, startTimestamp, endTimestamp

    The file can then be imported into excel or processed using command line tools.
"""

__version__ = '0.3'
__author__ = 'James Ponza'


import os

import json
import pandas as pd


BASEDIR='/home/kali/scripts/googlemaps/Antek/Takeout/Location History/Semantic Location History'
OUTFILE='antek_visit_history__fullcoords.csv'

out = open(OUTFILE,'w')
out.write("PlaceID,Name,Location,Latitude,Longitude,StartTime,EndTime\n")


visits = []
years = os.listdir(BASEDIR)

for year in years:
    files = os.listdir("%s/%s" % (BASEDIR,year))
    files = [ "%s/%s/%s" % (BASEDIR,year,file) for file in files if file.endswith("json") ]
    for file in files:
        print(file)
        f = open(file,encoding="utf-8")
        data = json.load(f)

        objects = data['timelineObjects']


        for o in objects:

            visit = {}

            if 'placeVisit' in o:
                v = o['placeVisit']

                if 'location' not in v or 'duration' not in v:
                    continue

                l = v['location']
                d = v['duration']

                for key in 'placeId', 'name','address','latitudeE7','longitudeE7':

                    val = ""

                    if key in l:
                        val = l[key]

                    if key in [ 'name', 'address' ]:
                        val = val.replace(',',' ')
                        val = val.replace('\n',' ')

                    if key in [ 'latitudeE7', 'longitudeE7' ]:
                        if val == "":
                            val = 0
                        val = int(val)
                        try:
                            val /= 10000000.0
                        except ValueError as e:
                            print( f'BAD [ValueError]: key={key} val={val}: {l}' )

                        # limit to 3
                        #val = '%.03f' % val
                        #val = '%.06f' % val
                        val = '%.7f' % val

                        key = key.replace('E7','')

                    visit[key] = val

                for key in 'startTimestampMs', 'endTimestampMs':
                    val = d[key]
                    val = pd.to_datetime( val, unit='ms' )

                    # remove milliseconds
                    if len(str(val)) == 26:
                        val = str(val)[:-7]

                    key = key.replace('Ms','')
                    visit[key] = val

                visits.append(visit)

                print(f"len(visits) = {len(visits)}\n")
        print(f"len(visits) = {len(visits)}\n")
print(f"len(visits) = {len(visits)}\n")

# total up the number of visits so we can record them
numvisits = {}
for v in visits:
    placeId = v['placeId']
    if placeId in numvisits:
        numvisits[placeId] += 1
    else:
        numvisits[placeId] = 1

# now write it all out to a file
for v in visits:
    v['visits'] = numvisits[v['placeId']]

    out.write("{visits},{placeId},{name},{address},{latitude},{longitude},{startTimestamp},{endTimestamp}\n".format(**v))


