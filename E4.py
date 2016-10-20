# -*- coding: utf-8 -*-
#Luis Cabañero Gómez
#Iván García Pulido

import matplotlib.pyplot as plt
import sys
import numpy as np

# Obtain coordinates
if(len(sys.argv) is not 2):
	print("Usage: python3 E4.py <file>")
	exit()
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


##KMeans

#Clustering execution
from sklearn.cluster import KMeans
from sklearn import metrics

k1=20
k2=40
steps=2
iterations=10
max_iter=50
tol=1e-04
random_state=0
y_kmL= []

ks=[]
sil=[]
for k in range(k1,k2,steps):
	km = KMeans(k, 'random', n_init = iterations, max_iter=max_iter, tol=tol,random_state=random_state)
	y_km=km.fit_predict(X)
	y_kmL.append(y_km)
	# Silhouette coefficient
	ks.append(k)
	sil.append(metrics.silhouette_score(X, y_km))

#Plot results
bestSil=max(sil)
i=sil.index(bestSil)
k=ks[i]
y_km=y_kmL[i]
print('Clusters: '+str(k))
print('Silhouette: %0.3f'%bestSil)

plt.scatter(ks, sil,c='blue', marker='o', s=20,)
plt.plot(ks, sil)
plt.show()

colors=['b','g','r','c','m','y','k','w']
markers=['o','v','^','+','x','8','s','p','*','h','D']
nMark=len(markers)
nCol=len(colors)
for i in range(k):
	plt.scatter(X[y_km==i,0], X[y_km==i,1],c=colors[i%nCol], marker=markers[(i//nCol)%nMark], s=15, label='cluster '+str(i))

plt.savefig('figure4-KMeans.png', dpi=1000)

##EM



##Spectral




