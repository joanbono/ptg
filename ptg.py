import argparse, requests
from datetime import datetime

'''
# Expected coordinates format:

1: 38.9136472N, 0.2337444W
2: 38.9131778N, 0.2333139W
3: 38.9125250N, 0.2329222W
4: 38.9117389N, 0.2323667W
5: 38.9115889N, 0.2317444W
6: 38.9113889N, 0.2309167W
7: 38.9112639N, 0.2303056W
8: 38.9111306N, 0.2297472W
9: 38.9111306N, 0.2293389W
10: 38.9112306N, 0.2288250W
11: 38.9113139N, 0.2282667W
12: 38.9113556N, 0.2279444W
'''

# Flags & args 
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--title", action="store", dest="title",
                    help="GPX Title", default="PTG_Generated-GPX", required=False)
parser.add_argument("-l", "--location", action="store", dest="location",
                    help="GPX Location", default="PTG_Virtual-Location", required=False)
parser.add_argument("-f", "--file", action="store", dest="filename",
                    help="Points file", required=True)
parser.add_argument("-v", "--version", action="version", version='%(prog)s 1.0.0')
args = parser.parse_args()

def gen_dummy_data(title, longdate, location):
    first_part = '''<?xml version="1.0" encoding="UTF-8"?>
    <gpx creator="PTG" version="1.1" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
    <metadata>
        <name>PTG - %s</name>
        <author>
        <name>PTG</name>
        <link href="https://www.github.com/joanbono/ptg">
        </link>
        </author>
        <link href="https://www.github.com/joanbono/ptg">
        <text>%s</text>
        </link>
        <time>%s</time>
    </metadata>
    <trk>
    <name>%s</name>
    <cmt>%s</cmt>
    <desc>%s</desc>
    <trkseg>'''%(title, title, longdate, title, location, location )

    last_part = '''</trkseg>
  </trk>
  </gpx>
  '''
    
    return first_part, last_part

def convert(tude):
    multiplier = 1 if tude[-1] in ['N', 'E'] else -1
    return multiplier * sum(float(x) / 60 ** n for n, x in enumerate(tude[:-1].split('-')))

def get_elevation(lat, long):
    query = ('https://api.open-elevation.com/api/v1/lookup'
             f'?locations={lat},{long}')
    r = requests.get(query).json()  
    return r['results'][0]['elevation']

def gen_track_data(lat,lon):
    track = '''<trkpt lat="%s" lon="%s">
        <ele>%s</ele>
        <time>%s</time>
      </trkpt>'''%(lat, lon,get_elevation(lat, lon),datetime.now().isoformat())
    return track 

def parsefile(filename):
    with open(filename, 'r+') as fp:
        for line in fp:
            ll = line.strip().split(':')
            print(gen_track_data(convert(ll[1].split(',')[0].replace(' ','')), convert(ll[1].split(',')[1].replace(' ',''))))

if __name__ == '__main__':

    first_part, last_part = gen_dummy_data(args.title, datetime.now().isoformat(), args.location)
    print(first_part)
    parsefile(args.filename)
    print(last_part)

