#!/usr/bin/python3
#Authors:
#Luis Cabañero Gómez
#Iván García Pulido

import sys
import xml.etree.ElementTree as ET
import csv

columns=['tipo', 'autonomia', 'provincia', 'matricula', 'causa', 'poblacion', 'fechahora_ini', 'nivel', 'carretera', 'pk_inicial', 'pk_final', 'sentido','longitud', 'latitud']
table=[columns]
if len(sys.argv) is not 3:
	print ("Usage: python3 E2.py <in_file> <out_file>")
else:
	xml=ET.parse(sys.argv[1])
	root=xml.getroot()
	cuenta=0
	for el in root:
		if el.findall('provincia')[0].text == 'BIZKAIA':
			table.append([el.findall(e)[0].text for e in columns])
			cuenta+=1 
	with open(sys.argv[2],'w') as f:
		writer=csv.writer(f)
		writer.writerows(table)
	print("Registers: "+str(cuenta))
