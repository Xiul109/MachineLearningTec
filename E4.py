# -*- coding: utf-8 -*-
#Luis Cabañero Gómez
#Iván García Pulido

import matplotlib.pyplot as plt
import sys
import numpy as np
import csv

#Plot function
def plot(sil, ks, y_xsL, X, name):
	bestSil=max(sil)
	i=sil.index(bestSil)
	k=ks[i]
	y_xs=y_xsL[i]
	print(name)
	print('Clusters: '+str(k))
	print('Silhouette: %0.3f'%bestSil)
	
	
	plt.scatter(ks, sil,c='blue', marker='o', s=20,)
	plt.plot(ks, sil)
	plt.title(name+'-sil')
	plt.savefig('figure4-'+name+'-sil.png', dpi=200)
	plt.clf()
	
	colors=['b','g','r','c','m','y','k','w']
	markers=['o','v','^','+','x','8','s','p','*','h','D']
	nMark=len(markers)
	nCol=len(colors)
	for i in range(k):
		plt.scatter(X[y_xs==i,0], X[y_xs==i,1],c=colors[i%nCol],marker=markers[(i//nCol)%nMark], s=15, label='cluster '+str(i))
	
	plt.title(name+'-clusts')
	plt.xlabel("Latitude")
	plt.ylabel("Longitude")
	plt.savefig('figure4-'+name+'-clusts.png', dpi=1000)
	plt.clf()

# Obtain coordinates
def dataExtraction():
	if(len(sys.argv) is not 2):
		print("Usage: python3 E4.py <file>")
		exit()
	else:
		csv_file=csv.DictReader(open(sys.argv[1]))

		X=[]
		nElements=0
		for row in csv_file:
			if(row['tipo']=='Accidente'):
				X.append([float(row['longitud']), float(row['latitud'])])
				nElements+=1
		print("Accidents: "+str(nElements))
		X=np.array(X)
		return X

#Program Execution
def algorithmExecution(algF,X, metrics, k1, k2, steps, name):
	
	y_algL= []
	
	ks=[]
	sil=[]
	for k in range(k1,k2,steps):
		alg=algF(k)
		y_alg=alg.fit_predict(X)
		y_algL.append(y_alg)
		# Silhouette coefficient
		ks.append(k)
		sil.append(metrics.silhouette_score(X, y_alg))
	
	return sil, ks, y_algL

X=dataExtraction()

k1=20
k2=41
steps=2

#KMeans
from sklearn.cluster import KMeans
from sklearn import metrics

iterations=10
max_iter=50
tol=1e-04
random_state=0

sil,ks, y=algorithmExecution(lambda k:KMeans(k, 'random', n_init = iterations, max_iter=max_iter, tol=tol,random_state=random_state),X, metrics,k1,k2,steps,'KMeans')
plot(sil, ks, y, X, 'KMeans')

#EM
from sklearn.mixture import GMM
covar_type='tied'

sil,ks, y=algorithmExecution(lambda k:GMM(n_components=k, covariance_type=covar_type, init_params='wc', n_iter=20),X, metrics,k1,k2,steps,'EM')
plot(sil, ks, y, X, 'EM')

#Spectral
from sklearn.cluster import SpectralClustering

sil,ks, y=algorithmExecution(lambda k: SpectralClustering(n_clusters=k, eigen_solver='arpack', affinity="nearest_neighbors"), X, metrics,k1,k2,steps,'Spectral')
plot(sil, ks, y, X, 'Spectral')




