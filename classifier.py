import nltk
import random
from music import Album, Song

albums = [Album('lyrics/kendrick/damn.txt'),
          Album('lyrics/taylor/red.txt'),
          Album('lyrics/taylor/1989.txt'),
          Album('lyrics/kendrick/tpab.txt')]
documents = [(song.words, album.artist) for album in albums for song in album]
# documents = [(song.words, album.artist) for song in album for album in albums]
random.shuffle(documents)

all_words = sum([album.fdist for album in albums], nltk.FreqDist())
# this looks at the most common words out of all albums
# not good at classifying for things such as the last line
# because the other words are contains=False, which
# makes it more likely for taylor to be selected
# TODO use highest tfidf words instead
word_features = all_words.most_common(500)

def document_features(document):
    """
    returns a dictionary mapping string features names to
    features

    Keyword arguments:
    document -- a list of words
    """
    document_words = set(document)
    features = dict()
    for word, count in word_features:
        features['contains({})'.format(word)] = word in document_words
    return features

feature_sets = [(document_features(d), c) for (d, c) in documents]

if __name__ == '__main__':
    split = int(len(feature_sets) / 3)
    train_set, validation_set = feature_sets[split:], feature_sets[:split]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    # print(classifier.classify(document_features(['yah'])))
    print("The Naive Bayes classifier correctly classifies the validation set with accuracy")
    print(nltk.classify.accuracy(classifier, validation_set))
    classifier.show_most_informative_features(10)

    # the algorithm predicts that this Vince Staples song is 
    # most similar to Kendrick Lamar's songs
    print("The classifier predicts this Vince Staples song to be similar to")
    test_song = Song('lyrics/vince/summertime06/08.txt')
    test_set = document_features(test_song.words)
    prediction = classifier.classify(test_set)
    print(prediction)
    print("with probability")
    prob_dist = classifier.prob_classify(test_set)
    print(prob_dist.prob(prediction))
