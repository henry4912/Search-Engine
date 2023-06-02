# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 13:27:59 2023

@author: Henry
"""

import json
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from tkinter import *
import main
import math
import time


# https://stackoverflow.com/questions/36367527/centering-widgets-in-tkinter-frame-using-pack
def search():
    index = getFinalIndex('final-index.json')
    docID = getDocID('docID.json')

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

    '''
    f = open('reportM2.txt', 'w+')
    f.write('Student Names: Derrick Jones, Sabrina Yang, Henry Ha, Christine Nguyen\n')
    f.write('Student IDs: 93547582, 27422353, 25602171, 56965805\n\n')
    f.write('Report M2:\n\n')
    f.close()
    '''

    def clicked():
        start = time.perf_counter()
        results = findResults(searchBox.get().lower(), index, docID)
        # reportWriteM2(searchBox.get(), results)
        finish = time.perf_counter() - start
        results += 'TIME: ' + str(finish)
        labelResults.configure(text=results)

    search = Button(frame2, text='Search', command=clicked)
    search.pack(side='left')
    frame2.place(relx=0.5, rely=0.25, anchor=N)

    window.mainloop()


def findResults(text, index, docID):
    sets = []
    results = ''
    porterStem = PorterStemmer()

    if len(text) == 0:
        return 'No results found\n\n'

    tokens = text.split()

    tokensNoStopwords = [t for t in tokens if t not in stopwords.words('english')]
    if len(tokensNoStopwords) != 0:
        tokens = tokensNoStopwords

    tokens = [porterStem.stem(t) for t in tokens]

    for token in tokens:
        if token not in index.keys():
            return 'No results found\n\n'
        else:
            bitLocation = index[token]
            with open('cs121-disk-final.json', 'r') as f:
                f.seek(bitLocation)
                entry = json.loads(f.readline())
                f.close()
            urlFreq = next(iter(entry.values()))
            urls = []
            for urlID in urlFreq.keys():
                urls.append(docID[urlID])
            sets.append(set(urls))

    intersection = list(set.intersection(*sets))
    if len(intersection) == 0:
        return 'No results found\n\n'
    elif len(intersection) > 10:
        for url in intersection[:10]:
            results += str(url) + '\n\n'
    else:
        for url in intersection:
            results += str(url) + '\n\n'

    return results


def calculateTF_IDFSum(text, index):
    score = {}
    with open('cs121-disk-final.json', 'r') as f:
        for t in text:
            if t in index.keys():
                bit = index[t]
                f.seek(bit)
                j = json.loads(f.readline())
                value = list(j.values())[0]
                for k, v in value.items():
                    if k in score.keys():
                        score[k] += v
                    else:
                        score[k] = v
        f.close()
    return score


def calculateCosine(text, normalizedIndex):
    queryFreq = {}
    for t in text:
        if t in queryFreq.keys():
            queryFreq[t] += 1
        else:
            queryFreq[t] = 1

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

        if ifAllFreqOne == False:
            normalize = 0
            for k, v in queryFreq.items():
                normalize += math.pow(v, 2)
            normalize = math.sqrt(normalize)
            for k, v in queryFreq.items():
                queryFreq[k] = v / normalize

        score = {}
        for t in text:
            if t in normalizedIndex.keys():
                bit = normalizedIndex[t]
                f.seek(bit)
                j = json.loads(f.readline())
                value = list(j.values())[0]
                for k, v in value.items():
                    if k in score.keys():
                        score[k] += v * queryFreq[t]
                    else:
                        score[k] = v * queryFreq[t]
        f.close()
    return score


def getFinalIndex(file):
    with open(file, 'r') as i:
        index = json.load(i)
        i.close()
    return index


def getDocID(file):
    with open(file, 'r') as d:
        docID = json.load(d)
        d.close()
    return docID


if __name__ == '__main__':
    search()