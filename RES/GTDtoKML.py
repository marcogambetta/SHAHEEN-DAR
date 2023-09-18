
import argparse
from pyproj import Proj
import simplekml
import pprint

parser = argparse.ArgumentParser(description='GDT to KML - Shot map created from Seismic Geometry')
parser.add_argument('-fi', type=str, help='GDT file (input)',required=True)
parser.add_argument('-fo', type=str, help='KML file (output)',required=False)
parser.add_argument('-d', type=str, help='if -d TRUE, it returns the list of shot points with planar coordinates (optional)')
args = parser.parse_args()


print ('\n'*100)

with open(args.fi,'r') as f:
    c = f.readlines()
for i,e in enumerate(c) :
 if e.strip() == "#23456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789":
    h= list(map(str.strip, c[0:i]))
    d= list(map(str.strip, c[i+1::]))
    break
for e in d:
    if e[0:4]=="H18 ":
        projection = list(filter(None,e.split(' ')))[-1]
    if e[0:4]=="H19 ":
        zone = list(filter(None,e.split(' ')))[-1]
encoding = {}
for e in h:
    k = e[0:27]
    v = e[27::]
    e = list(filter(None,v.split(' '))) #clean the input
    if k[0:2] != '#0':
     encoding[k[1::].rstrip()]={'ini':e[0],'end':e[1]}

myproj = Proj(proj=projection,zone=zone,ellps='WGS84', preserve_units=False)

Data ={}
for e in d:
    if e[0:1]=='R':
       rn =  e[int(encoding['RECEIVER NUMBER']['ini'])-1:int(encoding['RECEIVER NUMBER']['end'])].lstrip()
       k =  e[int(encoding['SPNB']['ini'])-1:int(encoding['SPNB']['end'])].lstrip()
       E =  float(e[int(encoding['RECEIVER X [EASTING]']['ini'])-1:int(encoding['RECEIVER X [EASTING]']['end'])])
       N =  float(e[int(encoding['RECEIVER Y [NORTHING]']['ini'])-1:int(encoding['RECEIVER Y [NORTHING]']['end'])])
       LO,LA = myproj(E,N,inverse = True)
       Data[k]={'RECEIVER_NUMBER':rn,'EASTING':E,'NORTHING':N, 'LONGITUDE':LO, 'LATITUDE':LA}

print("{0:>20s} : {1:<50s}".format('Input file',args.fi))
print ('\n')
print("{0:>20s} : {1:<50s}".format('Projection',projection))
print("{0:>20s} : {1:<50s}".format('Input file',zone))
print("{0:>20s} : {1:<50d}".format('Shots',len(Data.keys())))

kml = simplekml.Kml()

for i,k in enumerate(Data.keys()):
  LA = str(Data[k]['LATITUDE'])
  LO = str(Data[k]['LONGITUDE'])

  pnt = kml.newpoint(name=str(i), description="SHOT",
                     coords=[(Data[k]['LONGITUDE'], Data[k]['LATITUDE'])])  # lon, lat optional height

kml.save(args.fo)



#dump points planar coordinates if requested
if args.d == 'TRUE' :
 keys =list(Data.keys())
 print ('\nRECEIVER '+Data[keys[0]]['RECEIVER_NUMBER']+' LOCATION')
 print("{0:>10s} {1:>10s} {2:<12s} {3:<12s} {4:<16s} {5:<16s}".format('SHOT','RECEIVER','EASTING','NORTHING','LONGITUDE','LATITUDE'))
 for k in keys:
  print("{0:>10s} {1:>10s} {2:<12.2f} {3:<12.2f} {4:<16.12f} {5:<16.12f}".format(k,Data[k]['RECEIVER_NUMBER'],Data[k]['EASTING'],Data[k]['NORTHING'],Data[k]['LONGITUDE'],Data[k]['LATITUDE']))
