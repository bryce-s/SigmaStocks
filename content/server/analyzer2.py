from nltk import bigrams
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
import math

# globals
V = dict()  # vocabulary
D = 0  # number of documents (headlines)


def predict(trainingData, trainingCorrectData, testingData):
    vectorizer = TfidfVectorizer(ngram_range=(
        2, 2), min_df=1, use_idf=True, smooth_idf=True)
    # Vectorize the training data
    X_train = vectorizer.fit_transform(trainingData)

    # Vectorize the testing data
    X_test = vectorizer.transform(testingData)

    clf = svm.SVC(gamma=0.001, C=100.)

    # Train the SVM, optimized by Stochastic Gradient Descent
    # train_corpus_target is the correct values for each training data.
    clf.fit(X_train, trainingCorrectData)

    # Make predictions
    pred = clf.predict(X_test)
    print(pred)

# function that gets the total vocabulary in bigrams


def vocab(headlines):
    global D, V
    for headline in headlines:
        D += 1  # add to number of total headlines
        tokened = word_tokenize(headline)
        # make a list of bigrams from each headline
        bigram = list(bigrams(tokened))
        # add each bigram to the vocabulary
        for bgm in bigram:
            if bgm in V:
                V[bgm] += 1.0
            else:
                V[bgm] = 1.0

# function that takes in a list of headlines and returns the vectorized form of each one in a list.
# this essentially gets tf(w, d) for each headline.


def vectorize(headlines):
    global V
    vectors = list()
    for headline in headlines:
        # make a list of bigrams
        tokened = word_tokenize(headline)
        bigram = list(bigrams(tokened))
        one_hot = list()
        # for each vocabulary bigram, check if each one is in the headline bigrams
        for bgm in V:
            if bgm in bigram:
                one_hot.append(1)
            else:
                one_hot.append(0)
        vectors.append(one_hot)
    return vectors

# Now we calculate the idf(w, D) values and multiply them by the values in the one-hot vectors.
# idf(w, D) = log( (1 + |D|) / df(d, w) )
# df(d, w) = how many documents the word appears in


def normalize(vectors):
    global D
    for vector in vectors:
        for i in range(0, len(vectors)):
            # calculate the document frequency
            df = get_df(vectors, i)
            # cannot divide by 0 so we check:
            if df == 0:
                idf = 0
            else:
                idf = math.log((1 + D) / df, 10)
            # multiply already calculated tf values by idf values in the vector
            vector[i] *= idf
    return vectors


# finds how many documents the bigram at index in a vector occurs in
def get_df(vectors, index):
    total = 0
    for vector in vectors:
        if vector[index] == 1:
            total += 1
    return total


test = ["The movie was terrible.",
        "The movie was awesome!", "The movie was okay."]
vocab(test)
vectors = vectorize(test)
normals = normalize(vectors)


training = ["The music was terrible.",
            "The music was awesome!", "The music was okay."]
trainingCorrectData = [0, 1, 0]
# predict(training, trainingCorrectData, test)
