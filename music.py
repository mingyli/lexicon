import os
from nltk import RegexpTokenizer
from nltk import FreqDist
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import PlaintextCorpusReader
from nltk.stem.snowball import SnowballStemmer

import genius

pattern = r"""(?x)               # set flag to allow verbose regexps
              (?:[A-Z]\.)+       # abbreviations, e.g. U.S.A.
              |\d+(?:\.\d+)?%?   # numbers, incl. currency and percentages
              |\w+(?:[-’']\w+)*  # words w/ optional internal hyphens/apostrophe
              |(?:[+/\-@&*])     # special characters with meanings
           """
tokenizer = RegexpTokenizer(pattern)
punctuation = {'!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',',
        '-', '.', '/', '’', ':', ';', '<', '=', '>', '?', '@', '[', '\\',
        ']', '^', '_', '`', '{', '|', '}', '~'}
english_stopwords = set(stopwords.words('english'))
stemmer = SnowballStemmer('english')
wnl = WordNetLemmatizer()

def normalize(words, nostopwords=False, stem=False, lemmatize=False):
    """Return a generator to normalize words.
    
    Keyword arguments:
    words -- an iterable of strings
    nostopwords -- whether to include common English words (default False)

    note: lemmatizer is slower than stemming but its function is more 
          suitable for looking at song content

    >>> list(normalize(["Hello", "you're", "wonderful"], stem=True))
    ['hello', "you'r", 'wonder']
    """
    for word in words:
        word = word.lower()
        if word in punctuation:
            continue
        if nostopwords and word in english_stopwords:
            continue
        if stem:
            word = stemmer.stem(word)
        if lemmatize:
            word = wnl.lemmatize(word)
        yield word

class TextCollection:
    """
    A collection of words that supports various Python operations.
    This is constructed by passing in an iterable of words.

    >>> tc = TextCollection(['hello', 'world'])
    >>> 'hello' in tc
    True
    >>> tc.freq('world')
    0.5
    """

    def __init__(self, words):
        words = normalize(words)
        self.words = list(words)
        self.lexicon = set(self.words)
        self.fdist = FreqDist(self.words)

    def __contains__(self, word):
        return word in self.lexicon

    def __iter__(self):
        return iter(self.words)

    def __len__(self):
        return len(self.words)

    def count(self, word):
        return self.fdist[word]

    def freq(self, word):
        return self.fdist.freq(word)

    def wordcounts(self):
        return self.fdist.items()

class Album(TextCollection):
    """
    A TextCollection that is formed from text files containing
    the lyrics of an album.

    >>> damn = Album('lyrics/kendrick/damn.txt')
    >>> len(damn)
    14
    """

    def __init__(self, album_file):
        """
        if the album info is given by `lyrics/kendrick/damn.txt
        then the corpus path is given by `lyrics/kendrick/damn/`
        """

        # split into ('lyrics/kendrick/damn', '.txt')
        root, ext = os.path.splitext(album_file)
        root += '/'
        self.artist, self.title, song_titles = genius.parse_album_file(album_file)
        self.corpus = PlaintextCorpusReader(root,
                                            r'.*\.txt',
                                            word_tokenizer=tokenizer)
        super().__init__(self.corpus.words())
        self.tracks = [Song(root + fileid) for fileid in self.corpus.fileids()]

    def __len__(self):
        return len(self.tracks)

    def __iter__(self):
        return iter(self.tracks)

    def __getitem__(self, index):
        return self.tracks[index]

class Song(TextCollection):
    def __init__(self, fileid):
        self.fileid = fileid
        self.corpus = PlaintextCorpusReader('.', 
                                            fileid,
                                            word_tokenizer=tokenizer)
        super().__init__(self.corpus.words())

    def __repr__(self):
        title = self.corpus.sents()[0]
        return "<Song " + ' '.join(title) + ">"

    def __eq__(self, other):
        return self.fileid == other.fileid

    def __hash__(self):
        return hash(self.fileid)

if __name__ == '__main__':
    damn = Album('lyrics/kendrick/damn.txt')
