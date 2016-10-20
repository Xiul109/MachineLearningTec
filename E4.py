# -*- coding: utf-8 -*-
#Luis Cabañero Gómez
#Iván García Pulido

import matplotlib.pyplot as plt
import sys
import numpy as np

# Obtain coordinates
if(len(sys.argv) is not 2):
	print("Usage: python3 E4.py <file>")
else:
	xml=open(sys.argv[1],'r',encoding='latin-1')
	rows=xml.read().split('<incidenciaGeolocalizada>')[1:]
	latLen=len('<latitud>')
	lonLen=len('<longitud>')
	X=[]
	nElements=0
	for row in rows:
		if('<tipo>Accidente' in row):
			Xaux=[]
			Xaux.append(float(row[row.find('<longitud>')+lonLen:row.find('</longitud>')]))
			Xaux.append(float(row[row.find('<latitud>')+latLen:row.find('</latitud>')]))
			
			X.append(Xaux)
			nElements+=1
	print("Accidents: "+str(nElements))
	X=np.array(X)
	xml.close()
# plot the data
plt.scatter(X[:,0], X[:,1])
plt.show()

#Clustering execution
from sklearn.cluster import KMeans
from sklearn import metrics

k1=20
k2=100
steps=10
iterations=10
max_iter=50
tol=1e-04
random_state=0
y_km= None


for k in range(k1,k2,steps):
	km = KMeans(k, 'random', n_init = iterations, max_iter=max_iter, tol=tol,random_state=random_state)
	y_km = km.fit_predict(X)
	# Silhouette coefficient
	print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, y_km))

#Plot results
colors=['b','g','r','c','m','y','k','w']
markers=['o','v','^','+','x','8','s','p','*','h','D']
nMark=len(markers)
nCol=len(colors)
clust=max(y_km)
for i in range(-1,clust+1):
	plt.scatter(X[y_km==i,0], X[y_km==i,1],c=colors[i%nCol], marker=markers[(i//nCol)%nMark], s=15, label='cluster '+str(i)) 
#plt.legend()
plt.savefig('figure3.png', dpi=1000)

print('Clusters: '+str(clust))
