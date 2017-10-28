import json
import requests
from sklearn import metrics

with open('./testset.json', 'r') as f:
  dt_test = json.load(f)

X_test = []
y_test = []
y_predicted = []

for row in dt_test:
  X_test.append(row['text'].lower())
  y_test.append(row['intent'])
  r = requests.post("http://52.205.203.144:5000/parse", data='{"q":"'+row['text']+'", "model": "faq002"}')
  intent = eval(r.text)['intent']['name']
  print intent
  y_predicted.append(intent)

print 'Accuracy:',metrics.accuracy_score(y_test, y_predicted)
print 'Confusion matrix:', metrics.confusion_matrix(y_test, y_predicted)
