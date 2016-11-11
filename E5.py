# -*- coding: utf-8 -*-
#Luis Cabañero Gómez
#Iván García Pulido

import matplotlib.pyplot as plt
import sys
import numpy as np
import csv

# Obtain coordinates
accidentsData=[]

if(len(sys.argv) is not 3):
	print("Usage: python3 E3.py <input_file> <output_file>")
	exit()
else:
	csv_file=csv.DictReader(open(sys.argv[1]))
	
	inputData=list(csv_file)
	
	X=[]
	nElements=0
	for row in inputData:
		if(row['tipo']=='Accidente'):
			X.append([float(row['longitud']), float(row['latitud'])])
			accidentsData.append(row)
			nElements+=1
	print("Accidents: "+str(nElements))
	X=np.array(X)


#Clustering
from sklearn.cluster import KMeans
from sklearn import metrics


iterations=10
max_iter=50
tol=1e-04
random_state=0
k=40

clusterAlg=KMeans(k, 'random', n_init = iterations, max_iter=max_iter, tol=tol,random_state=random_state)
y=clusterAlg.fit_predict(X)

label='label'

for i in range(len(y)):
	accidentsData[i][label]=y[i]

#Feature Selection
outputData=[]

for i in range(min(y),max(y)+1):
	outputData.append({label:i})

clusters=[list(filter(lambda row:row[label]==i,accidentsData)) for i in range(min(y),max(y)+1)]

accidents='n_accidents'
time='Hora'
month='Mes'
road='Carretera'


causes=['Alcance','Atropello','Salida','Tijera camión','Vuelco']
hours=[i for i in range(0,24)]
months=[i for i in range(1,13)]

getHour=lambda fecha:int(fecha.split()[1].split(':')[0])
getMonth=lambda fecha:int(fecha.split()[0].split('-')[1])
def countRoads(rows):
	roads=[]
	for row in rows:
		if row['carretera'] not in roads:
			roads.append(row['carretera'])
	return len(roads)

features=[label,road,accidents]+[accidents+cause for cause in causes]+[accidents+time+str(i) for i in hours]+[accidents+month+str(i) for i in months]
for i in range(len(outputData)):
	cluster=clusters[i]
	element=outputData[i]
	#Number of accidents
	element[accidents]=len(cluster)
	#Number of accidents per cause
	for cause in causes:
		element[accidents+cause]=len(list(filter(lambda row:row['causa']==cause,cluster)))
	#Number of accidents per hour
	for hour in hours:
		element[accidents+time+str(hour)]=len(list(filter(lambda row:getHour(row['fechahora_ini'])==hour,cluster)))
	
	#Number of accidents per month
	for m in months:
		element[accidents+month+str(m)]=len(list(filter(lambda row:getMonth(row['fechahora_ini'])==m,cluster)))
	
	#Number of roads
	element[road]=countRoads(cluster)

#CSV Generation
with open(sys.argv[2],'w') as f:
	writer=csv.DictWriter(f,features)
	writer.writeheader()
	writer.writerows(outputData)


#PCA
from sklearn.decomposition import PCA
from sklearn import preprocessing
import sklearn.cluster
import numpy
#Transforming the list of dictionarys to a list of lists
states=[]
for element in outputData:
	state=[]
	for key, value in element.items():
		if key !='label':
			state.append(value)
	states.append(state)

#Normalization of the data
min_max_scaler = preprocessing.MinMaxScaler()
states = min_max_scaler.fit_transform(states)
        
#PCA Estimation
estimator = PCA (n_components = 2)
X_pca = estimator.fit_transform(states)

#Plotting
#k-means clustering
k = 3
centroids, labels, z =  sklearn.cluster.k_means(states, k, init="k-means++" )

#plot 
colors = ['b', 'r', 'g']
numbers = numpy.arange(len(X_pca))

fig, ax = plt.subplots()

for i in range(len(X_pca)):
    plt.text(X_pca[i][0], X_pca[i][1], numbers[i], color=colors[labels[i]]) 
   
plt.xlim(-2, 4)
plt.ylim(-0.5, 1.5)


ax.grid(True)
fig.tight_layout()

plt.savefig('E5-PCA.png', dpi=1000)


