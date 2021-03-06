#/usr/bin/python
import re
import json
import numpy as np
from glob import glob
from os.path import isfile
from newspaper import Article
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

import goose
g = goose.Goose()

ARTICLE_DIR = "money"
ARTICLE_DIR = "movie"
ARTICLE_DIR = "new_words"

articles = glob("./%s/*-*-article.json" % ARTICLE_DIR)
articles.sort()

companies = ["*"]
#companies = ['ibm','microsoft']
#companies = ['yuan','euro','yen','korea']
#companies = ['inception','the','frozen']
#companies = ['interstellar']

vectorizer = CountVectorizer(analyzer = "word",
                             tokenizer = None,
                             preprocessor = None,
                             stop_words = None,
                             max_features = 5000) 

clean_words = []

for company in companies:
    #path = "./%s/%s*-article.json" % (ARTICLE_DIR, company)
    path = "./%s/%s*-*.json" % (ARTICLE_DIR, company)

    for article in glob(path):
        print " ===> %s" % article
        bow = article.replace('/%s/' % ARTICLE_DIR,'/bow-%s/' % ARTICLE_DIR).replace('.json','-bow.json')

        #if isfile(bow):
        if False:
            print " [!] %s already exists" % bow
            continue
        else:
            print "[*] %s" % bow

        try:
            article_j = json.loads(open(article).read())
        except:
            continue

        for article_i in article_j:
            try:
                text = article_i['text']
                #print text
            except:
                continue

            if text == "":
                continue

            letters_only = re.sub("[^a-zA-Z]", " ", text) 
            words = letters_only.lower().split()
            stops = set(stopwords.words("english"))

            meaningful_words = [w for w in words if not w in stops]

            article_i['words'] = " ".join(meaningful_words)

        with open(bow, 'w') as f:
            json.dump(article_j, f)

    clean_words = [words for words in clean_words if words !='']

train_data_features = vectorizer.fit_transform(clean_words)
train_data_features = train_data_features.toarray()

vocab = vectorizer.get_feature_names()

dist = np.sum(train_data_features, axis=0)
for tag, count in zip(vocab, dist):
    print count, tag

test_data_features = vectorizer.transform(clean_words)
test_data_features = test_data_features.toarray()


