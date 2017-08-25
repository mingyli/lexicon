# import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import gensim
from gensim import corpora, models
from gensim.models.ldamodel import LdaModel
from gensim.corpora.textcorpus import TextDirectoryCorpus

from lexicon.music import Album
from lexicon.music import english_stopwords
from lexicon.music import stemmer


"""
tpab = TextDirectoryCorpus("lyrics/kendrick/tpab/", pattern=".+.txt")
id2word = tpab.dictionary
lda = LdaModel(corpus=tpab, id2word=id2word, num_topics=2)
lda.print_topics()
"""

# full = TextDirectoryCorpus("lyrics/", pattern=".+.txt")
# lda = LdaModel(corpus=full, id2word=full.dictionary, num_topics=2, passes=9)
# lda.print_topics()


albums = [Album('lyrics/kendrick/tpab.json'),
          Album('lyrics/kendrick/damn.json'),
          Album('lyrics/taylor/1989.json'),
          Album('lyrics/taylor/red.json')]

texts = [a.words for a in albums]
texts = [[stemmer.stem(word) for word in a.words if word not in english_stopwords] for a in albums]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

def get_topics(num_topics=2):
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dictionary, passes=20)

    print(ldamodel.print_topics(num_topics=num_topics, num_words=3))
