import spacy
nlp = spacy.load('en')

tokens = nlp(u'Net income was $9.4 million compared to the prior year of $2.7 million.')

for token in tokens:
  print token.text
#with open("../embeddings/100/dep.words", 'r') as f:
#    nlp.vocab.load_vectors(f)
#print 'loaded'

#nlp.vocab.dump_vectors("./100_dep.bin")
#print 'dumped'
