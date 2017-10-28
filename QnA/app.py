import logging
from logging.handlers import RotatingFileHandler
from flask import jsonify
from flask import Flask, render_template, request
from utils import *
from scipy.spatial.distance import cosine, euclidean
import numpy as np
import json

nlp = spacy.load('en', parser=False)
nlp.vocab.load_vectors_from_bin_loc("./100_bow10.bin")

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

@app.route('/classify', methods=["POST"])
def classify():
  js = request.get_json(force=True)
  app.logger.info('Request: %s' % json.dumps(js, indent=4))

  response = {}
  text_or = js['text']
  text = preprocess(text_or)

  text_emb = emb.transform([nlp(text)])[0]

# scores = [np.dot(text_emb, x_emb) for x_emb in X_emb]
# predicted_idx = np.argmax(scores)

  y_predicted = []
  y_score = []
  
  results_cos = {}
  for idx, x_emb in enumerate(X_emb):

    if np.sum(x_emb) == 0:
      print 'SKIP'
      continue
  
    if y[idx] not in results_cos:
      results_cos[y[idx]] = []
    
    results_cos[y[idx]].append(cosine(text_emb, x_emb))
   
  results_min_cos = {}
  for key, value in results_cos.iteritems():
    results_min_cos[key] = np.nanmin(value) 

  results_l = [(key, value) for key, value in results_min_cos.iteritems()]
  results_l = sorted(results_l,key=lambda x: x[1])
    
  score = results_l[0][1]
  label = results_l[0][0]
  syn = dataset[label][0]

  if score > 0.19:
    syn = 'Out of domain'
    response['closest'] = label
    label = '-1'
  else:
    if label == '26':
      c_scores = []
      for c_idx, comp in enumerate(work_with):
        c_scores.append(bleu_string_distance(comp, text))
      label += '_'+str(np.argmax(c_scores))
      syn +=' '+ work_with[np.argmax(c_scores)]
  
  response['text'] = text_or
  response['class'] = label
  response['score'] = 1.0-score
  response['paraphrase'] = syn
  
  app.logger.info('Response: %s' % json.dumps(response, indent=4))

  return jsonify(response)

@app.route('/test')
def test():
  return "server is up"

if __name__=='__main__':

  X,y = load_data('./faq_mod.json')
  app.logger.info('data is loaded')

  dataset = {}
  for idx, elem in enumerate(X):
    if y[idx] not in dataset:
      dataset[y[idx]] = []
    dataset[y[idx]].append(elem)

  with open('./work_with.json', 'r') as f:
    work_with = json.load(f)

  X_nlped = []
  for x in X:
    X_nlped.append(nlp(x))

  #emb = MeanEmbeddingVectorizerSpacy()
  emb = TfidfEmbeddingVectorizer()

  emb.fit(X_nlped,y)
  X_emb = emb.transform(X_nlped)

  handler = RotatingFileHandler('./foo.log', maxBytes=100000, backupCount=1)
  handler.setLevel(logging.INFO)
  app.logger.addHandler(handler)
  app.run(host='0.0.0.0', port=3030)
