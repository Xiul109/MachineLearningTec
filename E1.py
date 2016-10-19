#!/usr/bin/python3
#Authors:
#Luis Cabañero Gómez
#Iván García Pulido

import codecs
xml=codecs.open('IncidenciasTDTHist.xml', "r",encoding='utf-8', errors='ignore')
rows=xml.read().split('<raiz>')[1].replace('</raiz>','').split('<incidenciaGeolocalizada>')[1:]
xml.close()
cuenta=0
fichero=open('salida.xml','w')
fichero.close()
fichero=open('salida.xml','a')
for row in rows:
	if '<provincia>BIZKAIA' in row:
		cuenta+=1
		fichero.write('<incidenciaGeolocalizada>'+row+'\n')
fichero.close()
print("Registers: "+str(cuenta))
