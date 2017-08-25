
import gensim
from gensim import corpora, models
from gensim.models.ldamodel import LdaModel
from gensim.corpora.textcorpus import TextDirectoryCorpus

from lexicon.music import Album
from lexicon.music import english_stopwords
from lexicon.music import stemmer
from lexicon.tfidf import important_words


albums = [Album('lyrics/kendrick/tpab.json'),
          Album('lyrics/kendrick/damn.json'),
          Album('lyrics/taylor/1989.json'),
          Album('lyrics/taylor/red.json')]

for album in albums:
    print("The most important words in " + album.title + " are:")
    important = important_words(album, albums, 5)
    for term in important:
        print(term)
    print()


print("Here are some topics found in these albums.")

texts = [a.words for a in albums]
texts = [[stemmer.stem(word) for word in a.words if word not in english_stopwords] for a in albums]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

def get_topics(num_topics=2):
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dictionary, passes=20)
    topics = ldamodel.print_topics(num_topics=num_topics, num_words=3)
    for topic in topics:
        print(topic)

get_topics()
