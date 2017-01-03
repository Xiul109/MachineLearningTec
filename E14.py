import sys
import csv
import pydot
import numpy as np
from sklearn import tree
from sklearn.externals.six import StringIO

if(len(sys.argv) is not 4):
	print("Usage: python3 E14.py <cluster_file> <workroad_file> <pdf_file>")
	exit()

def count(zone,workroad_list):
	c=0
	for el in workroad_list:
		if el[1] == zone:
			c+=1
			workroad_list.remove(el)
	return c

cluster_file=list(csv.reader(open(sys.argv[1])))
feature_names=cluster_file[0][1:]
cluster_file=cluster_file[1:]
workroad_file=list(csv.reader(open(sys.argv[2])))[1:]
ranges=[[lambda x: x==0,0],[lambda x: x>=1 and x<10,1],[lambda x: x>=10 and x<25,2],[lambda x: x>=25 and x<50,3],[lambda x: x>=50,4]]
rangesStr=["0","[1-10)","[10-25)","[25-50)","[50-inf)"]

target=[]
for e in cluster_file:
	aux=count(e[0],workroad_file)
	for r in ranges:
		if r[0](aux):
			target.append(r[1])
			break
data=np.array(list(map(lambda x : x[1:],cluster_file)))
target=np.array(target)

#Decision Tree Training
treeClas=tree.DecisionTreeClassifier()
treeClas.fit(data, target)

#Decision Tree Plot
dot_data = StringIO()

tree.export_graphviz(treeClas, out_file=dot_data,feature_names=feature_names,class_names=rangesStr,filled=True, rounded=True, special_characters=True)

graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf(path=sys.argv[3])
