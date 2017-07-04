import os 
import logging
import re
import random
import numpy as np
import collections
from gensim.models import word2vec
import gensim
import json
import ConfigParser

cf = ConfigParser.ConfigParser()    
cf.read('conf.d/learning_embedding.conf')

file = cf.get('embedding', 'file')
result_dir = cf.get('embedding', 'result_dir')
embed_size = cf.getint('embedding', 'embed_size')
workers = cf.getint('embedding', 'workers')
max_vocab_size = cf.get('embedding', 'max_vocab_size')
sg = cf.getint('embedding', 'sg')

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

  
def trim_rule(word, count, min_count):
    return gensim.utils.RULE_KEEP if '_' in word else gensim.utils.RULE_DEFAULT 

def displayString(w):
    return re.sub(r'</?phrase>','',w)

concept_embeddings = {}

# sg is the training algorithm of learning embedding, where sg = 0 corresponds to CBOW, sg = 1 corresponds to skip-gram. 
# embed_size is the dimensionality of the learned embedding vectors.
# max_vocab_size is maximum num of vocabulary used during vocabulary building. It should be None or a number, e.g. 60000, where None means using all vocabulary.
# workers is num of threads used to learn the embedding.

if max_vocab_size == 'None':
    max_vocab_size = None
else:
    max_vocab_size = int(max_vocab_size)

if not os.path.exists(result_dir):
    os.makedirs(result_dir)

model = word2vec.Word2Vec(word2vec.LineSentence(file), size=embed_size,  workers=workers, max_vocab_size=max_vocab_size, 
  trim_rule = trim_rule, sg=sg)

max_vocab_size = -1 if max_vocab_size == None else max_vocab_size

concept_embeddings = {w:model.wv[w].tolist() for w in model.wv.index2word if '_' in w}


# model.save(result_dir + '/model_dimension%d_sg%d_max_vocab_size%d.model' % (embed_size, sg, max_vocab_size))
with open(result_dir+'/concept_embedding_dimension%d_sg%d_max_vocab_size%d.json' % (embed_size, sg, max_vocab_size), 'w') as f_out:
    json.dump(concept_embeddings, f_out)

