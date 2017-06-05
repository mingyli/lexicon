from nltk.corpus import PlaintextCorpusReader

if __name__ == '__main__':
    corpus_root = 'lyrics/kendrick/tpab/'
    wordlists = PlaintextCorpusReader(corpus_root, '.*\.txt')
    print(wordlists.fileids())
