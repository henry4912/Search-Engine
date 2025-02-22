# Student Names: Derrick Jones, Sabrina Yang, Henry Ha, Christine Nguyen
# Student IDs: 93547582, 27422353, 25602171, 56965805

import os, sys
from bs4 import BeautifulSoup
import json
import re
from nltk.stem import PorterStemmer
import math

'''
Loops through the directories and files under DEV to read and parse the json files.
Converts the json file into a dictionary and assigns the url a unique document ID.
Reads the contents of the page and stems and tokenizes the document.
The indexer is a dictionary with the key being the token and the value being
another dictionary that holds the document ID as the key and the frequency of the token
in that document as the value.

Finds which html tags the tokens were in and adds the corresponding weights 
as the html tag weights calculated in query.py

Source for reading into directories: https://stackoverflow.com/questions/39508469/reading-all-the-file-content-in-directory
Source for reading json into dictionary: https://www.geeksforgeeks.org/convert-json-to-dictionary-in-python/
Source for finding all headers in html: https://stackoverflow.com/questions/45062534/how-to-grab-all-headers-from-a-website-using-beautifulsoup
'''


def run():
    porterStem = PorterStemmer()
    idCounter = 1
    docID = {}
    fileCount = 0  # counts number of files before writing to disk
    totalFileCount = 0  # counts number of total files for tf-idf
    bitIndexes = []  # holds all the bit indexes for all files we wrote to
    validJsonCounter = 0  # valid json files
    frequencies = {}  # token frequencies

    assignmentFolder = os.getcwd() + '/DEV'
    for directories in os.listdir(assignmentFolder):
        subfolder = os.path.join(assignmentFolder, directories)
        for file in os.listdir(os.path.join(assignmentFolder, directories)):

            if (fileCount == 1000):
                fileCount = 0
                ind = writeToFile(frequencies, len(bitIndexes))
                bitIndexes.append(ind)
                frequencies = {}

            with open(os.path.join(subfolder, file), 'r') as j:
                jsonContentDictionary = json.load(j)
                currURL = ''

                for key, value in jsonContentDictionary.items():
                    if key == 'url':
                        currURL = value
                        validJsonCounter = validJsonCounter + 1
                        docID[str(idCounter)] = currURL

                    if key == 'content':
                        soup = BeautifulSoup(value, 'html.parser')

                        # finding headers
                        header = soup.find_all(re.compile('^h[1-6]$'))
                        headerText = []
                        for h in header:
                            if len(h) > 0:
                                text = re.findall(r'>(.*)<', str(h))
                                for t in text:
                                    t = t.replace('\n', '')
                                    while t.find('<') != -1:
                                        start = t.find('<')
                                        end = t.find('>', start)
                                        t = t[:start] + t[end + 1:]
                                    if len(t) > 0:
                                        headerText.append(t)

                        del header
                        headerTokens = []
                        for t in headerText:
                            hTokens = tokenizer(t)
                            for t2 in hTokens:
                                if len(t2) > 1:
                                    headerTokens.append(t2)
                        del headerText

                        # finding title text
                        titleTokens = findTags(soup, 'title')
                        # finding bold text
                        boldTokens = findTags(soup, 'b')
                        # finding strong (bold) text
                        strongTokens = findTags(soup, 'strong')
                        # finding italic text
                        italicTokens = findTags(soup, 'i')
                        # finding emphasized (italic) text
                        emphasizedTokens = findTags(soup, 'em')
                        # finding small text
                        # smallTokens = findTags(soup, 'small')
                        # assume that text not a part of these are body text

                        tokens = tokenizer(soup.text)

                        for t in tokens:
                            stemmedT = porterStem.stem(t)
                            if stemmedT in frequencies.keys():
                                if str(idCounter) in frequencies[stemmedT].keys():
                                    frequencies[stemmedT][str(idCounter)][0] += 1
                                else:
                                    frequencies[stemmedT][str(idCounter)] = [1, 0]
                            else:
                                frequencies[stemmedT] = {}
                                frequencies[stemmedT][str(idCounter)] = [1, 0]

                            # title = 1, headers = 0.85, bold/strong = .75, italic/emph = 0.5, other(small/body) = 0.1
                            if t in titleTokens:
                                frequencies[stemmedT][str(idCounter)][1] += 1
                                titleTokens.remove(t)
                            elif t in headerTokens:
                                frequencies[stemmedT][str(idCounter)][1] += 0.85
                                headerTokens.remove(t)
                            elif t in boldTokens:
                                frequencies[stemmedT][str(idCounter)][1] += 0.75
                                boldTokens.remove(t)
                            elif t in strongTokens:
                                frequencies[stemmedT][str(idCounter)][1] += 0.75
                                strongTokens.remove(t)
                            elif t in italicTokens:
                                frequencies[stemmedT][str(idCounter)][1] += 0.5
                                italicTokens.remove(t)
                            elif t in emphasizedTokens:
                                frequencies[stemmedT][str(idCounter)][1] += 0.5
                                emphasizedTokens.remove(t)
                            else:
                                frequencies[stemmedT][str(idCounter)][1] += 0.1

                fileCount += 1
                totalFileCount += 1
                idCounter += 1

    if len(frequencies) != 0:
        ind = writeToFile(frequencies, len(bitIndexes))
        bitIndexes.append(ind)

    with open('docID.json', 'w+') as d:
        json.dump(docID, d)
        d.close()

    mergeFiles(bitIndexes, totalFileCount)
    lengthNormalization()
    writeCacheWords()

    del frequencies
    del fileCount

    print('Done Indexing!')


'''
Tokenizes the contents of the files into alphanumeric tokens
'''


def tokenizer(contents):
    tokens = re.findall(r'[a-z0-9]+', contents.lower())
    return tokens


'''
Finds all the html tags that mark the tokens as important
Bold/strong, italics/emphasized, headers, title
'''


def findTags(soup, pattern):
    tag = soup.find_all(pattern)
    text = []
    for i in tag:
        if len(i) > 0:
            i = str(i).replace('\n', '')
            t = re.findall(r'>(.*)<', i)[0]
            while t.find('<') != -1:
                start = t.find('<')
                end = t.find('>', start)
                t = t[:start] + t[end + 1:]
            if len(t) > 0:
                text.append(t)
    del tag
    tokens = []
    for t in text:
        alphanumTokens = tokenizer(t)
        for t2 in alphanumTokens:
            if len(t2) > 1:
                tokens.append(t2)
    del text
    return tokens


'''
Writes the current index into a file
'''


def writeToFile(index, writeCount):
    fileName = 'cs121-disk' + str(writeCount) + '.json'
    bitIndex = {}
    index = dict(sorted(index.items()))

    with open(fileName, 'w+') as f:
        currBit = 0
        for k, v in index.items():
            bitIndex[k] = currBit
            temp = {k: v}
            json.dump(temp, f)
            f.write('\n')
            currBit += len(str(temp)) + 2

        f.close()

    return bitIndex


'''
Merges all files together to build a single file with the complete index.
Writes all files into a single file first with duplicates and then
creates the final file that merges those entries together.
'''


# https://stackoverflow.com/questions/7945182/opening-multiple-an-unspecified-number-of-files-at-once-and-ensuring-they-are
def mergeFiles(bitIndexes, totalFileCount):
    openFiles = []
    files = []
    bitIndex = {}
    finalIndex = {}

    for i in range(len(bitIndexes)):
        files.append('cs121-disk' + str(i) + '.json')
    try:
        for f in files:
            openFiles.append(open(f, 'r'))

        # merges all files into 1 file with duplicate tokens
        # makes the file pointer index hold list of pointers to
        # the duplicate entries to merge later
        with open('cs121-disk-duplicates.json', 'w+') as c:
            currBit = 0
            for f, b in zip(openFiles, bitIndexes):
                for k, v in b.items():

                    if k in bitIndex.keys():
                        bitIndex[k].append(currBit)
                    else:
                        bitIndex[k] = [currBit]

                    f.seek(v)
                    line = f.readline()
                    j = json.loads(line)
                    json.dump(j, c)
                    c.write('\n')
                    t = currBit
                    currBit += len(str(j)) + 2

            c.close()

        # writes into final file by merging entries in duplicates
        with open('cs121-disk-final.json', 'w+') as final:
            with open('cs121-disk-duplicates.json', 'r') as c:
                currBit = 0
                for k, v in bitIndex.items():
                    finalIndex[k] = currBit
                    if len(v) > 1:
                        c.seek(v[0])
                        t = json.loads(c.readline())
                        tValue = list(t.values())[0]
                        for i in v[1:]:
                            c.seek(i)
                            temp = list(json.loads(c.readline()).values())[0]
                            tValue.update(temp)

                        t[list(t.keys())[0]] = tValue
                        t = calculateTF_IDF(t, totalFileCount)
                        json.dump(t, final)

                    else:
                        c.seek(v[0])
                        t = json.loads(c.readline())
                        t = calculateTF_IDF(t, totalFileCount)
                        json.dump(t, final)

                    final.write('\n')
                    currBit += len(str(t)) + 2

                c.close()
            final.close()

    finally:
        for f in openFiles:
            f.close()

    with open('final-index.json', 'w+') as f:
        json.dump(finalIndex, f)
        f.close()


'''
Calculates the TF_IDF for all the documents under the token
'''


def calculateTF_IDF(t, totalFileCount):
    docuFreq = len(list(t.values())[0])
    for k, v in t.items():
        for doc, freq in v.items():
            tf_idf = (1 + math.log(freq[0])) * math.log(totalFileCount / docuFreq)
            t[k][doc][0] = tf_idf
    return t


'''
Normalizes the TF-IDF by going through the index file and adding
all the TF-IDF scores squared, then square roots and divides
each of the TF-IDF scores in final file.
'''


def lengthNormalization():
    normalizeBitLoc = {}
    currBit = 0

    with open('final-index.json', 'r') as ind:
        index = json.load(ind)
        ind.close()

    with open('docID.json', 'r') as doc:
        docID = json.load(doc)
        doc.close()

    # adds all the tf-idfs
    with open('cs121-disk-final.json', 'r') as f:
        doc_tfidf_sum = {}
        for token, bit in index.items():
            f.seek(bit)
            j = json.loads(f.readline())
            value = list(j.values())[0]
            for k, v in value.items():
                if k in doc_tfidf_sum.keys():
                    doc_tfidf_sum[k] += math.pow(v[0], 2)
                else:
                    doc_tfidf_sum[k] = math.pow(v[0], 2)
        f.close()

    for k, v in doc_tfidf_sum.items():
        doc_tfidf_sum[k] = math.sqrt(v)

    # normalizes the tf-idfs in the final file
    normalizedBitIndex = {}
    currBit = 0
    with open('cs121-disk-final.json', 'r') as f:
        with open('cs121-disk-final-normalized.json', 'w+') as n:
            for token, bit in index.items():
                normalizedBitIndex[token] = currBit
                f.seek(bit)
                j = json.loads(f.readline())
                value = list(j.values())[0]
                for k, v in value.items():
                    value[k][0] = v[0] / doc_tfidf_sum[k]
                j[token] = value
                json.dump(j, n)
                n.write('\n')
                currBit += len(str(j)) + 2
            n.close()
        f.close()

    with open('final-index-normalized.json', 'w+') as f:
        json.dump(normalizedBitIndex, f)
        f.close()


'''
Creates a dictionary with cache words: to, for, the, uci, computer, or, be, and, software, science
Return the dictionary (used in query.py)
'''


def writeCacheWords():
    porterStem = PorterStemmer()
    cacheWords = ['to', 'for', 'the', 'uci', 'computer', 'or', 'be', 'and', 'software', 'science']
    cacheWords = [porterStem.stem(t) for t in cacheWords]
    cache = {}

    with open('cs121-disk-final-normalized.json', 'r') as n:
        with open('final-index-normalized.json', 'r') as f:
            index = json.load(f)
            for word in cacheWords:
                bit = index[word]
                n.seek(bit)
                j = json.loads(n.readline())
                key = list(j.keys())[0]
                val = list(j.values())[0]
                cache[key] = val
    return cache


if __name__ == '__main__':
    run()