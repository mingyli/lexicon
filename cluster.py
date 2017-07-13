import random

def mean(s):
    assert len(s) > 0, 'cannot find mean of empty sequence'
    return sum(s) / len(s)

class Clusterer:
    """Uses Lloyd's algorithm to cluster vectors
    of words and associated numbers, such as tf-idf scores.
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
        >>> c.find_centroid(cluster)
        {'a': 4.0, 'b': 7.0}
        """

        centroid = {}
        for word in self.vocab:
            centroid[word] = mean([vec[word] for vec in cluster])
        return centroid

    def k_means(self, vecs, k, iterations=100):
        """Use k-means to group vectors into k clusters.

        >>> c = Clusterer({'a', 'b'})
        >>> vec0 = {'a': 5.0, 'b': 9.0}
        >>> vec1 = {'a': 3.0, 'b': 9.0}
        >>> vec2 = {'a': 4.0, 'b': 3.0}
        >>> vecs = [vec0, vec1, vec2]
        >>> c.k_means(vecs, 2, iterations=10)
        [{'a': 4.0, 'b': 3.0}, {'a': 4.0, 'b': 9.0}]
        """
        assert len(vecs) >= k, 'Not enough vectors to cluster'

        # select initial centroids randomly
        centroids = [vec for vec in random.sample(vecs, k)]

        for _ in range(iterations):
            clusters = self.group_by_centroid(vecs, centroids)
            centroids = [self.find_centroid(cluster) for cluster in clusters]
        return centroids
