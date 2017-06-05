from nltk import FreqDist
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords

if __name__ == '__main__':
    corpus_root = 'lyrics/kendrick/tpab/'
    album_corpus = PlaintextCorpusReader(corpus_root, r'.*\.txt')
    words = album_corpus.words()
    # use a set for stopwords for faster lookup
    stopword_set = set(stopwords.words('english'))
    # TODO: remove punctuation
    words = [word for word in words if word.lower() not in stopword_set]
    fdist = FreqDist(words)
    fdist.most_common(50)
