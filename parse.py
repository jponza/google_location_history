#!/usr/bin/env python
import os
import json
import pandas as pd

basedir="/home/kali/scripts/googlemaps/Takeout/Location History/Semantic Location History"

years = os.listdir(basedir)

visits = {}

out = open('visit_history__short_coords.csv','w')
#out = open('visit_history.csv','w')

out.write("PlaceID,Name,Location,Latitude,Longitude,StartTime,EndTime\n")

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
                        #print("key='%s' val='%s'" % (key,val))

                    if key in [ 'name', 'address' ]:
                        val = val.replace(',',' ')
                        val = val.replace('\n',' ')

                    if key in [ 'latitudeE7', 'longitudeE7' ]:
                        if val == '':
                            val = 0
                        val = int(val)
                        #print('val=%s' % val)
                        try:
                            val /= 10000000.0
                        except ValueError as e:
                            print("BAD [ValueError]: key=%s val=%s: %s" % (key,val,l))

                        # limit to 3
                        val = "%.03f" % val
                        #val = "%.06f" % val

                        key = key.replace('E7','')

                    visit[key] = val

                for key in 'startTimestampMs', 'endTimestampMs':
                    val = d[key]
                    val = pd.to_datetime( val, unit='ms' )
                    # remove milliseconds
                    print("val=%s" % val)
                    if len(str(val)) == 26:
                        val = str(val)[:-7]
                        print("val=%s" % val)
                    visit[key] = val

                visits.append(visit)

        for v in visits:
            out.write("%s,'%s','%s',%s,%s,%s,%s\n" % (v['placeId'], v['name'], v['address'], v['latitude'], v['longitude'], v['startTimestampMs'], v['endTimestampMs']))

