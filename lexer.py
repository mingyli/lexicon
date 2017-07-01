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
    tf = document.count(word)
    appearances = sum(word in doc for doc in collection)
    idf = math.log(len(collection) / appearances)
    return tf * idf

def important_words(album, n=None):
    """
    Get the n most important words in each song based on
    tf-idf score of each song with respect to the
    album. If n is None then all words will be collected.

    Returns a set mapping each song to a list of n Terms
    sorted by their tf-idf scores.

    >>> damn_album = Album('lyrics/kendrick/damn.json')
    >>> damn_important_words = important_words(damn_album, 5)
    >>> dna = damn_album[1]
    >>> terms = [term for term in damn_important_words[dna]]
    >>> sorted(term.word for term in terms)
    ['dna', 'ganja', 'gimme', 'got', 'inside']
    >>> max(terms, key=lambda t: t.tfidf).word
    'dna'
    """
    important_words = dict()

    for song in album:
        """Collects the n terms with highest tf-idf using a min heap."""
        terms = [] # as a heap
        for word in song.lexicon:
            tfidf_score = tfidf(word, song, album)
            new_term = Term(word=word, tfidf=tfidf_score)
            if len(terms) == n:
                # pushes new_term, then removes the term with lowest tf-idf
                heapq.heappushpop(terms, new_term)
            else:
                heapq.heappush(terms, new_term)

        important_words[song] = sorted(terms)

        """A slower implementation that collects all terms then sorts.
           Likely to be faster only for large n.
        important_words[song] = set()
        terms = []
        for word, count in song.wordcounts():
            tf = count
            appearances = sum(word in song for song in album)
            idf = math.log(len(album) / appearances)
            terms.append(Term(word=word, tfidf=tf * idf))

        terms.sort(key=lambda t: -t.tfidf)
        for i in range(n):
            important_words[song].add(terms[i])
        """

    return important_words


if __name__ == '__main__':
    import pprint
    damn_album = Album('lyrics/kendrick/damn.txt')
    damn_important_words = important_words(damn_album)
    pp = pprint.PrettyPrinter()
    print(damn_album[1])
    pp.pprint(damn_important_words[damn_album[1]])
    # damn_important_words = important_words(damn_album, 5)
    # for song in damn_album:
    #     print(song)
    #     pp.pprint(damn_important_words[song])
