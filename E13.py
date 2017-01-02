import csv
import sys
import pydot
import numpy as np
from sklearn import tree
from sklearn import preprocessing
from sklearn.externals.six import StringIO
class_names=['low','medium','high']
#Args checking
if(len(sys.argv) is not 3):
	print("Usage: python3 E13.py <input_training_file> <output_pdf_file>")
	exit()
#Files open
training=list(csv.reader(open(sys.argv[1])))
feature_names=training[0][1:-1]
training=training[1:]
#Training data separation
target=list(map(lambda x : x[-1],training))
le = preprocessing.LabelEncoder()
le.fit(class_names)

class_names=le.inverse_transform(np.sort(le.transform(class_names)))

target=le.transform(target)

data=np.array(list(map(lambda x : x[1:-1],training)))

#Decision Tree Training
treeClas=tree.DecisionTreeClassifier()
treeClas.fit(data, target)

#Decision Tree Plot
dot_data = StringIO()

tree.export_graphviz(treeClas, out_file=dot_data,feature_names=feature_names,class_names=class_names,filled=True, rounded=True, special_characters=True)

graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf(path=sys.argv[2])
