#!/usr/bin/env python
import csv
import simplekml
import sys


if len(sys.argv) != 2:
    print("Usage: createsimple.py FILENUM")


num=sys.argv[1]

#################################################################

infile=f'places.csv.{num}'
outfile=f'places.{num}.kml'

kml = simplekml.Kml()

with open(infile ,'r') as csvfile:
    placereader = csv.reader(csvfile, delimiter=',', quotechar="'")

    for row in placereader:
        (placeid,name,address,latitude,longitude,startts,endts) = row

        kml.newpoint(name=name, coords=[(latitude,longitude)])

kml.save(outfile)
