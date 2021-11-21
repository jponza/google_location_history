#!/usr/bin/env python
import os
import json

basedir="/home/kali/scripts/googlemaps/Takeout/Location History/Semantic Location History"

years = os.listdir(basedir)

visits = {}

out = open('visit_history.csv','w')

for year in years:
        files = os.listdir("%s/%s" % (basedir,year))
        files = [ "%s/%s/%s" % (basedir,year,file) for file in files if file.endswith("json") ]
        for file in files:
            print(file)
            f = open(file,)
            data = json.load(f)

            objects = data['timelineObjects']

            visits = []

            for o in objects:

                visit = {}

                if 'placeVisit' in o:
                    v = o['placeVisit']

                    if 'location' not in v or 'duration' not in v:
                        next

                    l = v['location']
                    d = v['duration']

                    for key in 'placeId', 'name','address','latitudeE7','longitudeE7':

                        val = ''

                        if key in l:
                            val = l[key]
                            print("key='%s' val='%s'" % (key,val))

                        if key in [ 'name', 'address' ]:
                            val = val.replace('\n',' ')

                        visit[key] = val

                    for key in 'startTimestampMs', 'endTimestampMs':
                        val = d[key]
                        visit[key] = val

                    visits.append(visit)

            for v in visits:
                out.write("%s,'%s','%s',%s,%s,%s,%s\n" % (v['placeId'], v['name'], v['address'], v['latitudeE7'], v['longitudeE7'], v['startTimestampMs'], v['endTimestampMs']))

