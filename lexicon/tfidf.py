import math
import random
import heapq
from collections import namedtuple
from multiprocessing import Pool
from functools import partial

from lexicon.music import Song, Album


class Term(namedtuple('Term', ['word', 'score'])):
    def __lt__(self, other):
        if self.score == other.score:
            return self.word < other.word
        return self.score < other.score

def exists(word, document):
    return word in document

def tfidf(word, document, collection, parallel=False):
    """Return the tf-idf score of a word
    in a document with respect to a collection of text.

    `parallel` should only be used for collections
    with a large number of documents because 
    of some overhead.

    TODO: offer more settings, such as count frequency vs
    proportional frequency

    >>> from lexicon.music import TextCollection
    >>> word = 'dolphin'
    >>> document0 = TextCollection(['dolphin', 'sea', 'world'])
    >>> document1 = TextCollection(['sea', 'world', 'fun'])
    >>> score = tfidf(word, document0, [document0, document1])
    >>> format(score, '0.2f')
    '0.69'
    >>> score = tfidf(word, document0, [document0, document1], parallel=True)
    >>> format(score, '0.2f')
    '0.69'
    """

    tf = document.count(word)
    if parallel:
        pool = Pool(len(collection))
        exist = partial(exists, word)
        appearances = pool.map(exist, collection)
        appearances = sum(appearances)
        pool.close()
        pool.join()
    else:
        appearances = sum(word in doc for doc in collection)
    idf = math.log(len(collection) / appearances)
    return tf * idf

def important_words(document, collection, n=None):
    """Return the n most important words in a document
    with respect to a collection based on the 
    highest tf-idf scores. The words are returned as
    namedtuples `Term`s.
    If n is None then all terms will be returned.

    >>> damn = Album('lyrics/kendrick/damn.json')
    >>> dna = damn[1]
    >>> terms = important_words(dna, damn, 5)
    >>> sorted(term.word for term in terms)
    ['dna', 'ganja', 'gimme', 'got', 'inside']
    >>> max(terms, key=lambda t: t.score).word
    'dna'
    """

    # Collect the n terms with highest tf-idf using divide and conquer.
    # Good if have access to entire document.
    # Expected runtime of O(len(document))
    def n_largest(terms, n):
        if len(terms) == 0 or n == 0:
            return []
        if len(terms) == n:
            return terms
        pivot = random.choice(terms)
        less, equal, more = [], [], []
        for term in terms:
            if term.score > pivot.score:
                more.append(term)
            elif term.score == pivot.score:
                equal.append(term)
            else:
                less.append(term)
        if len(more) >= n:
            return n_largest(more, n)
        if len(more) + len(equal) >= n:
            return more + equal[:n - len(more)]
        return more + equal + n_largest(less, n - len(more) - len(equal))

    terms = [Term(word, tfidf(word, document, collection)) for word in document.lexicon]
    return n_largest(terms, n)

    """
    # Collect the n terms with highest tf-idf using a min heap.
    # Good if words are fed by stream.
    # Runtime of O(len(document) * log n)
    terms = [] 
    for word in document.lexicon:
        tfidf_score = tfidf(word, document, collection)
        new_term = Term(word=word, score=tfidf_score)
        if len(terms) == n:
            heapq.heappushpop(terms, new_term)
        else:
            heapq.heappush(terms, new_term)
    return terms
    """

    """A slower implementation that collects all terms then sorts.
       Likely to be faster only for large n.
    terms = []
    for word, count in song.wordcounts():
        tf = count
        appearances = sum(word in song for song in album)
        idf = math.log(len(album) / appearances)
        terms.append(Term(word=word, score=tf * idf))

    terms.sort(key=lambda t: -t.tfidf)
    return terms[:n]
    """


if __name__ == '__main__':
    import pprint
    damn_album = Album('lyrics/kendrick/damn.txt')
    damn_important_words = important_words_album(damn_album)
    pp = pprint.PrettyPrinter()
    print(damn_album[1])
    pp.pprint(damn_important_words[damn_album[1]])
