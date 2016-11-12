import matplotlib.pyplot as plt
import sys
import numpy as np
import csv
from sklearn import preprocessing
import sklearn.neighbors
from scipy import cluster

csv_file=csv.reader(open('shit.csv'))
lists=list(csv_file)[1:]
lists=list(map(lambda x : list(map(float,x[1:])), lists))

min_max_scaler = preprocessing.MinMaxScaler()
lists = min_max_scaler.fit_transform(lists)


#metrics=['euclidean', 'manhattan', 'chebyshev','minkowski','wminkowski','seuclidean','mahalanobis']
#method=['complete', 'average', 'weighted','single','ward','median','centroid']
metrics=['manhattan']
method=['complete']

for me in metrics:
	dist = sklearn.neighbors.DistanceMetric.get_metric(me)
	matsim = dist.pairwise(lists)
	avSim = np.average(matsim)
	for m in method:
		clusters = cluster.hierarchy.linkage(matsim, method = m)
		cluster.hierarchy.dendrogram(clusters, color_threshold=42)
		plt.title(me+" "+m)
		#plt.savefig(me+" "+m, dpi=1000)
		plt.show()
		print('\n')
		

