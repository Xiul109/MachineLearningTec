import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn import neighbors
import sys

#Split the accidentsData leaving split_factor * Ndata as training data and  (1-split_factor) * Ndata as test data 
split_factor=0.6

if(len(sys.argv) is not 3):
	print("Usage: python3 E5.py <input_file> <output_file>")
	exit()

#Gets the K value
def getK():
	#Load Data
	data=[]
	csv_file=csv.DictReader(open(sys.argv[1]))
	for row in csv_file:
		data.append([float(row['longitud']), float(row['latitud']),int(row['label'])])

	#Split data
	trainX=[]
	trainY=[]
	testX=[]
	testY=[]
	for e in data:
		if np.random.random()<split_factor:
			trainX.append(e[:2])
			trainY.append(e[2])
		else:
			testX.append(e[:2])
			testY.append(e[2])
	testX=np.array(testX)
	trainX=np.array(trainX)
	
	#Apply KNN
	k=[]
	error=[]
	for i in range(1,100):
		clf = neighbors.KNeighborsClassifier(i)
		clf.fit(trainX,trainY)
		error.append(getErrorProp(clf.predict(testX),testY))
		k.append(i)
	plt.plot(k,error)
	plt.xlabel('K')
	plt.ylabel('Error')
	plt.show()
	return k[error.index(min(error))]

def getErrorProp(prediction,test):
	errors=0
	for i in range(len(prediction)):
		if prediction[i] != test[i]:
			errors+=1
	return errors/len(prediction)

k=getK()
csv_file=csv.DictReader(open('out_file.csv'))
data=list(csv_file)
worksX=[]
outData=[]
for row in data:
	if(row['tipo']=='Obras'):
		outData.append(row)
		worksX.append([float(row['longitud']), float(row['latitud'])])
worksX=np.array(worksX)

csv_file=csv.DictReader(open(sys.argv[2]))
X=[]
y=[]
for row in csv_file:
	X.append([float(row['longitud']), float(row['latitud'])])
	y.append(int(row['label']))

clf = neighbors.KNeighborsClassifier(k)
clf.fit(X,y)
worksY=clf.predict(worksX)

for i in range(len(outData)):
	outData[i]['label']=worksY[i]

#Write works Data in a csv
with open('works.csv', 'w') as csvfile:
	fieldnames = list(outData[0].keys())
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	writer.writeheader()
	writer.writerows(outData)

