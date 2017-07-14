import random
from statistics import mean

class HashableDict(dict):
    """A dictionary that can be hashed for use in
    sets or other dictionaries.

    Warning: The `hash` function is not consistent across
    different machines or between different interpreter sessions.
    This is stable only during a single interpreter lifetime.

    >>> hd0 = HashableDict([('a', 1)])
    >>> hd1 = HashableDict([('b', 2)])
    >>> d = {hd0: 3, hd1: 4}
    >>> d[hd0], d[hd1]
    (3, 4)
    >>> hd2 = HashableDict([('a', 1)]) # identical to hd0
    >>> hd0 == hd2
    True
    >>> d[hd2]
    3
    """

    def __hash__(self):
        return hash(frozenset(self.items()))


class WordScoreVector(HashableDict):
    def __init__(self, name, key_value_pairs):
        self.name = name
        super().__init__(key_value_pairs)

    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        return 0

    def __str__(self):
        return self.name

    def __repr__(self):
        return "WordScoreVector({})".format(self.name)

    def __eq__(self, other):
        return self.name == other.name


class Clusterer:
    """Uses Lloyd's algorithm to cluster vectors
    of words and associated numbers, such as tf-idf scores.

    >>> vocab = {'a', 'b'}
    >>> c = Clusterer(vocab)
    """

    def __init__(self, vocab):
        self.vocab = set(vocab)

    def sq_dist(self, vec0, vec1):
        """Return the squared Euclidean distance between two
        vectors of tf-idf scores.
        
        >>> c = Clusterer({'a', 'b'})
        >>> vocab = {'a', 'b'}
        >>> vec0 = {'a': 5.0, 'b': 9.0}
        >>> vec1 = {'a': 3.0, 'b': 8.0}
        >>> c.sq_dist(vec0, vec1)
        5.0
        """
        return sum((vec0[w] - vec1[w]) ** 2 for w in self.vocab)

    def find_closest(self, vec, centroids):
        """Return the centroid that is closest to the given vector.

        >>> c = Clusterer({'a', 'b'})
        >>> vec = {'a': 5.0, 'b': 9.0}
        >>> centroids = [{'a': 4.0, 'b': 4.0}, {'a': 5.0, 'b': 10.0}]
        >>> c.find_closest(vec, centroids)
        {'a': 5.0, 'b': 10.0}
        """
        return min(centroids, key=lambda c: self.sq_dist(vec, c))

    def group_by_centroid(self, vecs, centroids):
        """Return a list of clusters, each of which is a list
        of vectors that are closest to the same centroid.

        TODO: worry about speed + correctness

        >>> c = Clusterer({'a', 'b'})
        >>> vec0 = {'a': 5.0, 'b': 9.0}
        >>> vec1 = {'a': 3.0, 'b': 8.0}
        >>> vec2 = {'a': 3.0, 'b': 3.0}
        >>> vecs = [vec0, vec1, vec2]
        >>> cen0 = {'a': 4.0, 'b': 4.0}
        >>> cen1 = {'a': 5.0, 'b': 10.0}
        >>> centroids = [cen0, cen1]
        >>> clusters = c.group_by_centroid(vecs, centroids)
        >>> clusters[0] == [vec2]
        True
        >>> clusters[1] == [vec0, vec1]
        True
        """

        closest = []
        for vec in vecs:
            closest.append((vec, self.find_closest(vec, centroids)))
        return [[vec for vec, centroid in closest if centroid == c] for c in centroids]
        clusters = []
        for vec, centroid in closest:
            if centroid not in clusters:
                clusters[centroid] = set()
            clusters[centroid].add(vec)
        return clusters

    def find_centroid(self, cluster):
        """Return the vector that is the mean of
        all vectors in a cluster.

        >>> c = Clusterer({'a', 'b'})
        >>> vec0 = {'a': 5.0, 'b': 9.0}
        >>> vec1 = {'a': 3.0, 'b': 9.0}
        >>> vec2 = {'a': 4.0, 'b': 3.0}
        >>> cluster = [vec0, vec1, vec2]
        >>> c.find_centroid(cluster) == {'a': 4.0, 'b': 7.0}
        True
        """

        centroid = {}
        for word in self.vocab:
            centroid[word] = mean([vec[word] for vec in cluster])
        return centroid

    def k_means(self, vecs, k, iterations=100):
        """Use k-means to group vectors into k clusters.
        Returns the centroids and their corresponding clusters.

        >>> c = Clusterer({'a', 'b'})
        >>> vec0 = {'a': 5.0, 'b': 9.0}
        >>> vec1 = {'a': 3.0, 'b': 9.0}
        >>> vec2 = {'a': 4.0, 'b': 3.0}
        >>> vecs = [vec0, vec1, vec2]
        >>> centroids, clusters = c.k_means(vecs, 2, iterations=10)
        >>> for centroid, cluster in zip(centroids, clusters):
        ...     for vec in cluster:
        ...         assert centroid == c.find_closest(vec, centroids)
        """
        assert len(vecs) >= k, 'Not enough vectors to cluster'

        # select initial centroids randomly
        centroids = [vec for vec in random.sample(vecs, k)]

        for _ in range(iterations):
            clusters = self.group_by_centroid(vecs, centroids)
            centroids = [self.find_centroid(cluster) for cluster in clusters]
        return centroids, clusters

if __name__ == '__main__':
    from music import Album, Song
    from tfidf import tfidf, important_words, Term
    albums = [Album('lyrics/kendrick/damn.json'),
              Album('lyrics/taylor/red.json')]

    # collect the n most important words from each song
    # `important_words` is based on highest tfidf score
    all_songs = [song for album in albums for song in album]
    word_features = set()
    for song in all_songs:
        imp_words = important_words(song, all_songs, n=2)
        word_features.update([t.word for t in imp_words])

    clusterer = Clusterer(word_features)
    wsvecs = []
    for song in all_songs:
        terms = []
        for word in word_features:
            terms.append(Term(word=word, tfidf=tfidf(word, song, all_songs)))
        wsvecs.append(WordScoreVector(song.title, terms))

    centroids, clusters = clusterer.k_means(wsvecs, 4)
    for cluster in clusters:
        print(len(cluster))
