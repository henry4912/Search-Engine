# Student Names: Derrick Jones, Sabrina Yang, Henry Ha, Christine Nguyen
# Student IDs: 93547582, 27422353, 25602171, 56965805

import os, sys
from bs4 import BeautifulSoup
import json
import re
from nltk.stem import PorterStemmer
from tkinter import *
import math

'''
Loops through the directories and files under DEV to read and parse the json files.
Converts the json file into a dictionary and assigns the url a unique document ID.
Reads the contents of the page and stems and tokenizes the document.
The indexer is a dictionary with the key being the token and the value being
another dictionary that holds the document ID as the key and the frequency of the token
in that document as the value.


Source for reading into directories: https://stackoverflow.com/questions/39508469/reading-all-the-file-content-in-directory
Source for reading json into dictionary: https://www.geeksforgeeks.org/convert-json-to-dictionary-in-python/
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

    assignmentFolder = os.getcwd() + '/ANALYST'
    for directories in os.listdir(assignmentFolder):
        subfolder = os.path.join(assignmentFolder, directories)
        for file in os.listdir(os.path.join(assignmentFolder, directories)):

            if (fileCount == 1500):
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
                        tokens = tokenizer(soup.text)

                        for t in tokens:
                            t = porterStem.stem(t)
                            if t in frequencies.keys():
                                if str(idCounter) in frequencies[t].keys():
                                    frequencies[t][str(idCounter)] += 1
                                else:
                                    frequencies[t][str(idCounter)] = 1
                            else:
                                frequencies[t] = {}
                                frequencies[t][str(idCounter)] = 1
                fileCount += 1
                totalFileCount += 1
                idCounter += 1

    if len(frequencies) != 0:
        ind = writeToFile(frequencies, len(bitIndexes))
        bitIndexes.append(ind)

    # if len(bitIndexes) > 1:
    #    mergeFiles(bitIndexes, totalFileCount)
    mergeFiles(bitIndexes, totalFileCount)

    reportWriteM1(idCounter, validJsonCounter, frequencies)

    del frequencies
    del fileCount

    search(frequencies, docID)


'''
Tokenizes the contents of the files into alphanumeric tokens
'''


def tokenizer(contents):
    tokens = re.findall(r'[a-z0-9]+', contents.lower())
    return tokens


# https://stackoverflow.com/questions/36367527/centering-widgets-in-tkinter-frame-using-pack
def search(freq, docID):
    window = Tk()
    window.title('Yet Another Search Engine')
    window.geometry('1000x700')
    labelTitle = Label(window, text='Search Engine')
    labelTitle.place(relx=0.5, rely=0.2, anchor=CENTER)

    frame1 = Frame(window)
    labelResults = Label(frame1)
    labelResults.pack(side='bottom')
    frame1.place(relx=0.5, rely=0.6, anchor=S)

    frame2 = Frame(window)
    searchBox = Entry(frame2, width=30)
    searchBox.pack(side='left')

    f = open('reportM2.txt', 'w+')
    f.write('Student Names: Derrick Jones, Sabrina Yang, Henry Ha, Christine Nguyen\n')
    f.write('Student IDs: 93547582, 27422353, 25602171, 56965805\n\n')
    f.write('Report M2:\n\n')
    f.close()

    def clicked():
        results = findResults(searchBox.get().lower(), freq, docID)
        reportWriteM2(searchBox.get(), results)
        labelResults.configure(text=results)

    search = Button(frame2, text='Search', command=clicked)
    search.pack(side='left')
    frame2.place(relx=0.5, rely=0.25, anchor=N)

    window.mainloop()


def findResults(text, freq, docID):
    sets = []
    results = ''
    porterStem = PorterStemmer()
    tokens = text.split()
    tokens = [porterStem.stem(t) for t in tokens]

    for token in tokens:
        if token not in freq.keys():
            return 'No results found'
        else:
            urlFreq = freq[token]
            urls = []
            for urlID in urlFreq.keys():
                urls.append(docID[urlID])
            sets.append(set(urls))

    intersection = list(set.intersection(*sets))
    if len(intersection) == 0:
        return 'No results found'
    elif len(intersection) > 5:
        for url in intersection[:5]:
            results += str(url) + '\n\n'
    else:
        for url in urlFreq:
            results += str(url) + '\n\n'

    return results


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
    '''    
    it = iter(bitIndex.items())
    for i in range(5):
        print(next(it))
    exit(0)
    '''

    return bitIndex


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
        # merge = mergeDictionaries(bitIndexes) # dont know which file its in then

        # merges all files into 1 file with duplicate tokens
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

        # write to final file with no duplicates and token dicts all merged
        # add tf-idf
        with open('bitIndex.txt', 'w+') as bitw:
            bitw.write(str(bitIndex))

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
                        # t = calculateTF_IDF(t, totalFileCount)
                        json.dump(t, final)

                    final.write('\n')
                    currBit += len(str(t)) + 2

                c.close()
            final.close()

    finally:
        for f in openFiles:
            f.close()

    return finalIndex


def mergeDictionaries(dicts):
    mergedDict = {}
    for d in dicts:
        for k, v in d.items():
            if k in mergedDict.keys():
                mergedDict[k].append(v)
            else:
                mergedDict[k] = [v]
    return mergedDict


def calculateTF_IDF(tValue, totalFileCount):
    docuFreq = len(tValue.keys())
    for k, v in tValue.items():
        for doc, freq in v.items():
            tf_idf = (1 + math.log(freq)) * math.log(totalFileCount / docuFreq)
            tValue[k][doc] = tf_idf
    return tValue


'''
Writes the report with the number of indexed documents, unique tokens,
and size of the indexer
'''


def reportWriteM1(idCounter, validJsonCounter, frequencies):
    f = open("reportM1.txt", "w+")
    f.write('Student Names: Derrick Jones, Sabrina Yang, Henry Ha, Christine Nguyen\n')
    f.write('Student IDs: 93547582, 27422353, 25602171, 56965805\n\n')
    f.write('Report M1:\n\n')

    f.write('\nNumber of Indexed Documents: ' + str(validJsonCounter))
    f.write('\nNumber of unique tokens: ' + str(len(frequencies)))
    indexSize = sys.getsizeof(frequencies) / 1000
    f.write("\nTotal size of index on disk: " + str(indexSize) + " KB")
    f.close()


def reportWriteM2(entry, results):
    f = open('reportM2.txt', 'a')
    f.write(entry + '\n')
    f.write(results)
    f.write('--------------------------------------------------------------\n')
    f.close()


if __name__ == '__main__':
    run()