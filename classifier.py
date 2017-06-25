import nltk
import random
from music import Album

damn = Album('lyrics/kendrick/damn.txt')
red = Album('lyrics/taylor/red.txt')
_1989 = Album('lyrics/taylor/1989.txt')
tpab = Album('lyrics/kendrick/tpab.txt')
documents = [(song.words, 'kendrick') for song in damn]
documents += [(song.words, 'taylor') for song in red]
documents += [(song.words, 'taylor') for song in _1989]
documents += [(song.words, 'kendrick') for song in tpab]
random.shuffle(documents)

all_words = damn.fdist + red.fdist + _1989.fdist + tpab.fdist
# TODO this looks at the most common words out of all albums
# not good at classifying for things such as the last line
# because the other 1999 words are contains=False, which
# makes it more likely for taylor to be selected
word_features = all_words.most_common(2000)

def document_features(document):
    document_words = set(document)
    features = dict()
    for word, count in word_features:
        features['contains({})'.format(word)] = word in document_words
    return features

feature_sets = [(document_features(d), c) for (d, c) in documents]

if __name__ == '__main__':
    split = int(len(feature_sets) / 5)
    train_set, test_set = feature_sets[split:], feature_sets[:split]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    # print(classifier.classify(document_features(['yah'])))
    print(nltk.classify.accuracy(classifier, test_set))
    classifier.show_most_informative_features(5)
