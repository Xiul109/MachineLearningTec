#!/usr/bin/python3
#Authors:
#Luis Cabañero Gómez
#Iván García Pulido

import sys
import xml.etree.ElementTree as ET
import csv

columns=['tipo', 'causa', 'poblacion', 'fechahora_ini', 'nivel', 'carretera', 'pk_inicial', 'pk_final', 'sentido','longitud', 'latitud']
table=[columns]

arglen=len(sys.argv)
if (arglen==4 or arglen==6):
	
	min_lat=min_lon=-sys.maxsize
	max_lat=max_lon=sys.maxsize
	in_file=2
	out_file=3
	if len(sys.argv) is 6:
		in_file=4
		out_file=5
		min_lat=float(sys.argv[2].split(':')[0])
		max_lat=float(sys.argv[2].split(':')[1])
		min_lon=float(sys.argv[3].split(':')[0])
		max_lon=float(sys.argv[3].split(':')[1])
	
	
	xml=ET.parse(sys.argv[in_file])
	root=xml.getroot()
	cuenta=0
	for el in root:
		lat=el.findall('latitud')[0].text
		alt=el.findall('longitud')[0].text
		if lat is not None and alt is not None:
			lat=float(lat)
			alt=float(alt)
		if el.findall('provincia')[0].text == sys.argv[1] and min_lat<=lat<=max_lat and min_lon<=alt<=max_lon:
			table.append([el.findall(e)[0].text for e in columns])
			cuenta+=1 
	with open(sys.argv[out_file],'w') as f:
		writer=csv.writer(f)
		writer.writerows(table)
	print("Registers: "+str(cuenta))
else:
	print ("Usage: python3 E2.py <provice> [<min lon>:<max lon> <min lat>:<max lat>] <in_file> <out_file>")
	print ("Example python3 E2.py BIZKAIA 42.9:43.5 -3.5:-2.2 in_file.xml out_file.csv")
	exit()
