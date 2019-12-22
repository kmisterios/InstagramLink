import pickle
import math
from nltk.tokenize import TweetTokenizer
import string
import os
import sys
import numpy as np

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

tokenizer = TweetTokenizer()


with open('firstapp/model_stuff/model_10000.sav', 'rb') as f:
    loaded_model = pickle.load(f)


def comments_preprocessing(line):
    line = ' '.join(tokenizer.tokenize(line.lower()))
    chrs = string.ascii_lowercase + ' '
    new_line = ''
    for ch in line:
        if ch in chrs:
            new_line += ch
    new_line = ' '.join(tokenizer.tokenize(new_line.lower()))
    return new_line


def computeReviewTFDict(review):
    # Counts the number of times the word appears in review
    reviewTFDict = {}
    for word in review.split():
        if word in reviewTFDict:
            reviewTFDict[word] += 1
        else:
            reviewTFDict[word] = 1
    return reviewTFDict


with open('firstapp/model_stuff/idfDict.txt', 'rb') as fp:
    idfDict = pickle.load(fp)


def computeReviewTFIDFDict(reviewTFDict):
    reviewTFIDFDict = {}
    # For each word in the review, we multiply its tf and its idf.
    for word in reviewTFDict:
        if word in reviewTFDict and word in idfDict:
            reviewTFIDFDict[word] = reviewTFDict[word] * idfDict[word]
    return reviewTFIDFDict


with open('firstapp/model_stuff/wordDict.txt', 'rb') as fp:
    wordDict = pickle.load(fp)

wordDict_mapping = {}
for i, word in enumerate(wordDict):
    wordDict_mapping[word] = i


def computeTFIDFVector(review):
    tfidfVector = [0.0] * len(wordDict)

    # For each unique word, if it is in the review, store its TF-IDF value.
    for word in review:
        if word in wordDict:
            tfidfVector[wordDict_mapping[word]] = review[word]
    return tfidfVector


def do_things(lines):
    if len(lines) == 0:
        return str(0) + '%', 0, 0
    processed_lines = [comments_preprocessing(line) for line in lines]
    tfDict_test = [computeReviewTFDict(review) for review in processed_lines]
    tfidfDict_test = [computeReviewTFIDFDict(review) for review in tfDict_test]
    tfidfVector_test = [computeTFIDFVector(review) for review in tfidfDict_test]
    result = loaded_model.predict(tfidfVector_test)
    result = np.array(result)
    print(result)
    if (result.sum()* 100) % len(result) != 0:
        return str(round(result.sum()/len(result)*100, 1)) + '%', result.sum(), len(result) -result.sum()
    else:
        return str(int(round(result.sum()/len(result)*100))) + '%', result.sum(), len(result) -result.sum()
        
