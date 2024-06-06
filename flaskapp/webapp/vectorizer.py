import re 
import os
import pickle 

from sklearn.feature_extraction.text import HashingVectorizer

cur_dir = os.path.dirname(__file__)
stop = pickle.load(open(os.path.join(cur_dir, 'admin/pickle_objects', 'stopwords.pkl'), 'rb'))

def tokenizer(sentence):
    sentence = re.sub('<[^>]*>', '', sentence)
    emoticons = re.findall('(?::|;|=) (?:-) ?(?:\)|\(|D|P)', sentence.lower())
    sentence = re.sub('[\W]+', ' ', sentence.lower()) + ' '.join(emoticons).replace('-', '')
    tokenized = [ word for word in sentence.split() if word not in stop ]
    
    return tokenized

vect = HashingVectorizer(decode_error='ignore', n_features=2**21,
                        preprocessor=None, tokenizer=tokenizer)