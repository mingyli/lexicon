import math
import heapq
from collections import namedtuple

from music import Song, Album

class Term(namedtuple('Term', ['word', 'tfidf'])):
    def __lt__(self, other):
        if self.tfidf == other.tfidf:
            return self.word < other.word
        return self.tfidf < other.tfidf

def tfidf(word, document, collection):
    """Return the tf-idf score of a word
    in a document with respect to a collection of text.

    TODO: offer more settings, such as count frequency vs
    proportional frequency

    >>> from music import TextCollection
    >>> word = 'dolphin'
    >>> document0 = TextCollection(['dolphin', 'sea', 'world'])
    >>> document1 = TextCollection(['sea', 'world', 'fun'])
    >>> score = tfidf(word, document0, [document0, document1])
    >>> format(score, '0.2f')
    '0.69'
    """

    tf = document.count(word)
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
    >>> max(terms, key=lambda t: t.tfidf).word
    'dna'
    """

    # Collects the n terms with highest tf-idf using a min heap.
    terms = [] # as a min-heap
    for word in document.lexicon:
        tfidf_score = tfidf(word, document, collection)
        new_term = Term(word=word, tfidf=tfidf_score)
        if len(terms) == n:
            heapq.heappushpop(terms, new_term)
        else:
            heapq.heappush(terms, new_term)

    """A slower implementation that collects all terms then sorts.
       Likely to be faster only for large n.
    terms = []
    for word, count in song.wordcounts():
        tf = count
        appearances = sum(word in song for song in album)
        idf = math.log(len(album) / appearances)
        terms.append(Term(word=word, tfidf=tf * idf))

    terms.sort(key=lambda t: -t.tfidf)
    return terms[:n]
    """
    return terms


if __name__ == '__main__':
    import pprint
    damn_album = Album('lyrics/kendrick/damn.txt')
    damn_important_words = important_words_album(damn_album)
    pp = pprint.PrettyPrinter()
    print(damn_album[1])
    pp.pprint(damn_important_words[damn_album[1]])
