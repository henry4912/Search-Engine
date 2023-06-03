# Student Names: Derrick Jones, Sabrina Yang, Henry Ha, Christine Nguyen
# Student IDs: 93547582, 27422353, 25602171, 56965805

import json
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from tkinter import *
import main
import math
import time

'''
Creates local GUI using TKinter and prompts user for query
'''


# https://stackoverflow.com/questions/36367527/centering-widgets-in-tkinter-frame-using-pack
def search():
    normalizedIndex = getFinalIndex('final-index-normalized.json')
    docID = getDocID('docID.json')
    cache = getCacheWords()

    window = Tk()
    window.title('Yet Another Search Engine')
    window.geometry('1250x950')
    labelTitle = Label(window, text='Search Engine')
    labelTitle.place(relx=0.5, rely=0.2, anchor=CENTER)

    frame1 = Frame(window)
    labelResults = Label(frame1)
    labelResults.pack(side='bottom')
    frame1.place(relx=0.5, rely=0.65, anchor=S)

    frame2 = Frame(window)
    searchBox = Entry(frame2, width=30)
    searchBox.pack(side='left')

    def clicked():
        start = time.perf_counter()
        results = findResults(searchBox.get().lower(), normalizedIndex, docID, cache)
        finish = time.perf_counter() - start
        results += 'TIME: ' + str(finish)
        labelResults.configure(text=results)

    search = Button(frame2, text='Search', command=clicked)
    search.pack(side='left')
    frame2.place(relx=0.5, rely=0.25, anchor=N)

    window.mainloop()


'''
Processes the query and calls calculation methods for tf-idf, cos, and html tag
weights to get the score for each document that can be shown to the user
'''


def findResults(text, normalizedIndex, docID, cache):
    sets = []
    results = ''
    porterStem = PorterStemmer()

    if len(text) == 0:
        return 'No results found\n\n'

    tokens = tokenizer(text)

    tokensNoStopwords = [t for t in tokens if t not in stopwords.words('english')]
    if len(tokensNoStopwords) != 0:
        tokens = tokensNoStopwords

    tokens = [porterStem.stem(t) for t in tokens]

    queryFreq = {}
    for t in tokens:
        if t in queryFreq.keys():
            queryFreq[t] += 1
        else:
            queryFreq[t] = 1

    urls = getURLsToRank(queryFreq, normalizedIndex, 10, cache)

    tf_idf_score = calculateTF_IDFSum(queryFreq, normalizedIndex, urls, cache)
    html_score = calclateHTMLTagWeights(queryFreq, normalizedIndex, urls, cache)
    cos_score = calculateCosine(queryFreq, normalizedIndex, urls, cache)

    score = {}
    for i in tf_idf_score.keys():
        score[i] = 0.35 * (tf_idf_score[i]) + 0.25 * (html_score[i]) + 0.4 * (cos_score[i])

    if len(score) == 0:
        return 'No results found\n\n'

    if len(score) > 10:
        sorted_score = dict(sorted(score.items(), key=lambda x: x[1], reverse=True)[:10])
    else:
        sorted_score = dict(sorted(score.items(), key=lambda x: x[1], reverse=True))

    results = ''
    for k in sorted_score.keys():
        results += docID[k] + '\n\n'

    return results


'''
Retrieves the valid documents to calculate scoring.
This is done by finding documents that have the most terms out of the query
'''


# https://stackoverflow.com/questions/26871866/print-highest-value-in-dict-with-key
def getURLsToRank(queryFreq, normalizedIndex, k, cache):
    tokens = {}
    resultDict = {}
    with open('cs121-disk-final-normalized.json', 'r') as f:
        for t in queryFreq.keys():
            bit = normalizedIndex[t]
            f.seek(bit)
            j = json.loads(f.readline())
            docids = list(j.values())[0].keys()
            for did in docids:
                if did in resultDict.keys():
                    resultDict[did] += 1
                else:
                    resultDict[did] = 1

    if len(resultDict) > 10:
        resultDict = dict(sorted(resultDict.items(), key=lambda x: x[1], reverse=True)[:100])
    else:
        resultDict = dict(sorted(resultDict.items(), key=lambda x: x[1], reverse=True))

    urls = []
    for key in resultDict.keys():
        urls.append(key)

    return urls


'''
Calculates the tf-idf scoring by adding all the tf-idf values
'''


def calculateTF_IDFSum(queryFreq, normalizedIndex, urls, cache):
    score = {}
    with open('cs121-disk-final-normalized.json', 'r') as f:
        for t in queryFreq.keys():
            if t in cache.keys():
                value = cache[t]
                weight = 1
                if queryFreq[t] > 1:
                    weight = queryFreq[t]
                for u in urls:
                    if u not in value.keys():
                        break
                    if u in score.keys():
                        score[u] += value[u][0] * weight
                    else:
                        score[u] = value[u][0] * weight

            elif t in normalizedIndex.keys():
                bit = normalizedIndex[t]
                f.seek(bit)
                j = json.loads(f.readline())
                value = list(j.values())[0]
                weight = 1
                if queryFreq[t] > 1:
                    weight = queryFreq[t]
                for u in urls:
                    if u not in value.keys():
                        break
                    if u in score.keys():
                        score[u] += value[u][0] * weight
                    else:
                        score[u] = value[u][0] * weight
        f.close()
    return score


'''
Calculates the html tag weights by adding the weights for which html
tag the tokens were in.
'''


def calclateHTMLTagWeights(queryFreq, normalizedIndex, urls, cache):
    score = {}
    with open('cs121-disk-final-normalized.json', 'r') as f:
        for t in queryFreq.keys():
            if t in cache.keys():
                value = cache[t]
                weight = 1
                if queryFreq[t] > 1:
                    weight = queryFreq[t]
                for u in urls:
                    if u not in value.keys():
                        break
                    if u in score.keys():
                        score[u] += value[u][1] * weight
                    else:
                        score[u] = value[u][1] * weight

            elif t in normalizedIndex.keys():
                bit = normalizedIndex[t]
                f.seek(bit)
                j = json.loads(f.readline())
                value = list(j.values())[0]
                weight = 1
                if queryFreq[t] > 1:
                    weight = queryFreq[t]
                for u in urls:
                    if u not in value.keys():
                        break
                    if u in score.keys():
                        score[u] += value[u][1] * weight
                    else:
                        score[u] = value[u][1] * weight
        f.close()
    return score


'''
Calculates the cosine similarity between the query and relevant documents
using tf-idf scoring
'''


def calculateCosine(queryFreq, normalizedIndex, urls, cache):
    with open('cs121-disk-final-normalized.json', 'r') as f:
        ifAllFreqOne = True
        for k, v in queryFreq.items():
            if v > 1:
                ifAllFreqOne = False
            if k in normalizedIndex.keys():
                bit = normalizedIndex[k]
                f.seek(bit)
                j = json.loads(f.readline())
                value = list(j.values())[0]
                tf_idf = (1 + math.log(v)) * math.log(len(normalizedIndex) / len(value))
            else:
                tf_idf = 1 + math.log(v)
            queryFreq[k] = tf_idf

        normalize = 0
        for k, v in queryFreq.items():
            normalize += math.pow(v, 2)
        normalize = math.sqrt(normalize)
        for k, v in queryFreq.items():
            queryFreq[k] = v / normalize

        score = {}
        for t in queryFreq.keys():
            if t in cache.keys():
                value = cache[t]
                weight = 1
                if queryFreq[t] > 1:
                    weight = queryFreq[t]
                for u in urls:
                    if u not in value.keys():
                        break
                    if u in score.keys():
                        score[u] += value[u][0] * queryFreq[t] * weight
                    else:
                        score[u] = value[u][0] * queryFreq[t] * weight

            elif t in normalizedIndex.keys():
                bit = normalizedIndex[t]
                f.seek(bit)
                j = json.loads(f.readline())
                value = list(j.values())[0]
                weight = 1
                if queryFreq[t] > 1:
                    weight = queryFreq[t]
                for u in urls:
                    if u not in value.keys():
                        break
                    if u in score.keys():
                        score[u] += value[u][0] * queryFreq[t] * weight
                    else:
                        score[u] = value[u][0] * queryFreq[t] * weight

        f.close()
    return score


'''
Tokenizes the contents of the files into alphanumeric tokens
'''


def tokenizer(contents):
    tokens = re.findall(r'[a-z0-9]+', contents.lower())
    return tokens


'''
Retrieves the pointer index for the file with the complete index
'''


def getFinalIndex(file):
    with open(file, 'r') as i:
        index = json.load(i)
        i.close()
    return index


'''
Retrieves the document IDs for the index
'''


def getDocID(file):
    with open(file, 'r') as d:
        docID = json.load(d)
        d.close()
    return docID


'''
Retrieves cache words by calling function in main.py
'''


def getCacheWords():
    return main.writeCacheWords()


if __name__ == '__main__':
    search()