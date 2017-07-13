import nltk
import random
from music import Album, Song
from lexer import important_words

albums = [Album('lyrics/kendrick/damn.json'),
          Album('lyrics/taylor/red.json'),
          Album('lyrics/taylor/1989.json'),
          Album('lyrics/kendrick/tpab.json')]
documents = [(song.words, album.artist) for album in albums for song in album]
random.shuffle(documents)

all_words = sum([album.fdist for album in albums], nltk.FreqDist())
# word_features = all_words.most_common(500)

# collect the n most important words from each song
# based on highest tfidf score
word_features = set()
for album in albums:
    for song in album:
        imp_words = important_words(song, all_words, n=10)
        word_features.update([t.word for t in imp_words])

def document_features(document):
    """Returns a dictionary mapping 
    string features names to features.

    Keyword arguments:
    document -- a list of words
    """
    document_words = set(document)
    features = dict()
    for word in word_features:
        features['contains({})'.format(word)] = word in document_words
    return features

feature_sets = [(document_features(d), c) for (d, c) in documents]

def predict_song(test_song):
    print("The classifier predicts {} to be similar to".format(test_song.title))
    test_set = document_features(test_song.words)
    prediction = classifier.classify(test_set)
    print(prediction)
    print("with probability")
    prob_dist = classifier.prob_classify(test_set)
    print(prob_dist.prob(prediction))


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
    test_song = Song('lyrics/vince/summertime06/08.txt', title='SAMO')
    predict_song(test_song)

    bft = Album('lyrics/vince/bigfishtheory.json')
    for song in bft:
        predict_song(song)
        print()
