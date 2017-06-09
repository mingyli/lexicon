from nltk import FreqDist
from nltk import RegexpTokenizer
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import TwitterCorpusReader
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.tokenize.regexp import WhitespaceTokenizer

if __name__ == '__main__':
    corpus_root = 'lyrics/kendrick/tpab/'
    album_corpus = PlaintextCorpusReader(corpus_root, r'.*\.txt', word_tokenizer=WhitespaceTokenizer())
    # album_corpus = TwitterCorpusReader(corpus_root, r'.*\.txt')
    words = album_corpus.words()
    # use a set for stopwords for faster lookup
    stopword_set = set(stopwords.words('english'))
    # > my_tokenizer = nltk.RegexpTokenizer(regex)
    punctuation = {'!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
            ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'}
    words = [word for word in words if word.lower() not in stopword_set]
    # words = [word for word in words if word not in punctuation]
    fdist = FreqDist(words)
    fdist.most_common(50)
    # fdist.plot(50, cumulative=True)
