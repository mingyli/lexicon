import math
from nltk import FreqDist
from nltk import RegexpTokenizer
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

punctuation = {'!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
        ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'}
stopword_set = set(stopwords.words('english'))
stemmer = PorterStemmer()

class Song:
    def __init__(self, lyrics):
        self.lexicon = set(lyrics)
        self.fdist = FreqDist(lyrics)

    def contains(self, word):
        return word in self.lexicon

    def term_freq(self, word):
        return self.fdist[word]

def normalize(words):
    words = [word.lower() for word in words]
    words = [word for word in words if word not in punctuation]
    # words = [word for word in words if word not in stopword_set]
    words = [stemmer.stem(word) for word in words]
    return words

if __name__ == '__main__':
    corpus_root = 'lyrics/kendrick/tpab/'

    pattern = r"""(?x)                   # set flag to allow verbose regexps
                  (?:[A-Z]\.)+           # abbreviations, e.g. U.S.A.
                  |\d+(?:\.\d+)?%?       # numbers, incl. currency and percentages
                  |\w+(?:[-']\w+)*       # words w/ optional internal hyphens/apostrophe
                  |(?:[+/\-@&*])         # special characters with meanings
               """
    tokenizer = RegexpTokenizer(pattern, gaps=False)
    album_corpus = PlaintextCorpusReader(corpus_root, r'.*\.txt', word_tokenizer=tokenizer)
    
    album_lyrics = normalize(album_corpus.words())
    album_fdist = FreqDist(album_lyrics)


    album = []
    for fileid in album_corpus.fileids():
        lyrics = normalize(album_corpus.words(fileid))
        album.append(Song(lyrics))



    def tf_idf(word, l_fdist):
        tf = l_fdist[word]
        appearances = 0
        return tf


    tuples = []
    for word, freq in album[4].fdist.most_common():
        appearances = sum(song.contains(word) for song in album)
        idf = math.log(len(album) / appearances)
        # print(word, freq, idf, freq * idf)
        tuples.append((word, freq, idf, freq * idf))

    tuples.sort(key=lambda t: t[3])
    for t in tuples:
        print(t)
