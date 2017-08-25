import itertools
import nltk
import random
from nltk import FreqDist
from nltk import ConditionalFreqDist
from nltk.corpus import PlaintextCorpusReader
from nltk.probability import ConditionalProbDist
from nltk.probability import MLEProbDist


# from music import Album
from lexicon.music import tokenizer

def pairs(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

album = PlaintextCorpusReader('lyrics/kendrick/', 
                              r'.*\.txt', 
                              word_tokenizer=tokenizer)

# def generate_model(cfdist, word, num=15):
def generate_model(cpdist, word, num=15):
    for i in range(num):
        print(word)
        # word = cfdist[word].max()
        # words = list(cfdist[word])
        # word = random.choice(words)
        word = cpdist[word].generate()


"""
model = {}
# for word0, word1 in pairs(album.words()):
for word0, word1 in nltk.bigrams(album.words()):
    word0, word1 = word0.lower(), word1.lower()
    if word0 not in model:
        model[word0] = FreqDist()
    model[word0][word1] += 1
"""

bigrams = nltk.bigrams(word.lower() for word in album.words())
cfd = ConditionalFreqDist(bigrams)
cpd = ConditionalProbDist(cfd, MLEProbDist)

seed = 'the'
# generate_model(cfd, seed)
generate_model(cpd, seed)
