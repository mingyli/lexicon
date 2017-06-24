import math
from collections import namedtuple
from queue import PriorityQueue

from music import Song, Album


Term = namedtuple('Term', ['word', 'tfidf'])
Term.__lt__ = lambda t1, t2: t1.tfidf < t2.tfidf


def important_words(album, n=5):
    """
    Get the n most important words in each song based on
    tf-idf score of each song with respect to the
    album.

    Returns a set mapping each song to n words and their
    tf-idf scores.

    >>> damn_album = Album('lyrics/kendrick/damn/')
    >>> damn_important_words = important_words(damn_album)
    >>> blood = damn_album[0]
    >>> terms = [term for term in damn_important_words[blood]]
    >>> sorted(term.word for term in terms)
    ['blind', 'decide', 'she', 'something', 'wickedness']
    >>> max(terms, key=lambda t: t.tfidf).word
    'something'
    """
    important_words = dict()

    for song in album:
        important_words[song] = set()
        # terms = PriorityQueue(n)
        # for word, count in song.wordcounts():
        #     # calculate tf-idf of word in song with respect to album
        #     tf = count
        #     appearances = sum(word in song for song in album)
        #     idf = math.log(len(album) / appearances)
        #     new_term = Term(word=word, tfidf=tf * idf)
        #     if terms.full():
        #         old_term = terms.get()
        #         terms.put(max([new_term, old_term]))
        #     else:
        #         terms.put(new_term)

        # for i in range(terms.qsize()):
        #     print(terms.get())

        terms = []
        for word, count in song.wordcounts():
            tf = count
            appearances = sum(word in song for song in album)
            idf = math.log(len(album) / appearances)
            terms.append(Term(word=word, tfidf=tf * idf))

        terms.sort(key=lambda t: -t.tfidf)
        for i in range(n):
            important_words[song].add(terms[i])

    return important_words


if __name__ == '__main__':
    damn_album = Album('lyrics/kendrick/damn/')
    damn_important_words = important_words(damn_album)
    import pprint
    pp = pprint.PrettyPrinter()
    for song in damn_album:
        print(song)
        pp.pprint(damn_important_words[song])
