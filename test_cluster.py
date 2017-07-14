import random
import numpy as np

from sklearn.cluster import KMeans
from clusterer import Clusterer

vocab = {'a', 'b', 'c'}
c = Clusterer(vocab)

def rando():
    result = {}
    for w in vocab:
        result[w] = random.random()
    return result

vecs = []
for i in range(100):
    vecs.append(rando())

centroids, clusters = c.k_means(vecs, 2)

for centroid, cluster in zip(centroids, clusters):
    for vec in cluster:
        assert centroid == c.find_closest(vec, centroids)



"""Instead of dictionaries, have positioned words"""
vocab = list(vocab)

def dict2list(d):
    return [d.get(w, 0) for w in vocab]

X = np.array([dict2list(d) for d in vecs])
kmeans = KMeans(n_clusters=2).fit(X)


if __name__ == '__main__':
    from music import Album, Song
    from tfidf import tfidf, important_words, Term
    albums = [Album('lyrics/kendrick/damn.json'),
              Album('lyrics/taylor/red.json')]

    # collect the n most important words from each song
    # `important_words` is based on highest tfidf score
    all_songs = [song for album in albums for song in album]
    vocab = set()
    for song in all_songs:
        imp_words = important_words(song, all_songs, n=10)
        vocab.update([t.word for t in imp_words])

    vocab = list(vocab)
    wsvecs = []
    for song in all_songs:
        terms = []
        for word in vocab:
            terms.append(Term(word=word, tfidf=tfidf(word, song, all_songs)))
        wsvecs.append(dict(terms))
    X = np.array([dict2list(v) for v in wsvecs])
    kmeans = KMeans(n_clusters=2).fit(X)
