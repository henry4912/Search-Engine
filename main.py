# Student Names: Derrick Jones, Sabrina Yang, Henry Ha, Christine Nguyen
# Student IDs: 93547582, 27422353, 25602171, 56965805

import os,sys
from bs4 import BeautifulSoup
import json
import re
from nltk.stem import PorterStemmer

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
    validJsonCounter = 0  # valid json files
    frequencies = {}  # token frequencies
    assignmentFolder = os.getcwd() + '/DEV'
    for directories in os.listdir(assignmentFolder):
        subfolder = os.path.join(assignmentFolder, directories)
        for file in os.listdir(os.path.join(assignmentFolder, directories)):
            with open(os.path.join(subfolder, file), 'r') as j:
                jsonContentDictionary = json.load(j)
                currURL = ''
                for key, value in jsonContentDictionary.items():
                    if key == 'url':
                        currURL = value
                        validJsonCounter = validJsonCounter + 1
                        docID[currURL] = idCounter
                    if key == 'content':
                        soup = BeautifulSoup(value, 'html.parser')
                        tokens = tokenizer(soup.text)
                        for t in tokens:
                            t = porterStem.stem(t)
                            if t in frequencies.keys():
                                if currURL in frequencies[t].keys():
                                    frequencies[t][idCounter] += 1
                                else:
                                    frequencies[t][idCounter] = 1
                            else:
                                frequencies[t] = {}
                                frequencies[t][idCounter] = 1
                    
                idCounter += 1
    reportWrite(idCounter, validJsonCounter, frequencies)

'''
Tokenizes the contents of the files into alphanumeric tokens
'''
def tokenizer(contents):
    tokens = re.findall(r'[a-z0-9]+', contents.lower())
    return tokens

'''
Writes the report with the number of indexed documents, unique tokens,
and size of the indexer
'''
def reportWrite(idCounter, validJsonCounter, frequencies):
    f = open("report.txt", "w+")
    f.write('Student Names: Derrick Jones, Sabrina Yang, Henry Ha, Christine Nguyen\n')
    f.write('Student IDs: 93547582, 27422353, 25602171, 56965805\n\n')
    f.write('Report:\n\n')
    f.write('\nNumber of documents: ' + str(idCounter))
    f.write('\nNumber of Indexed Documents: ' + str(validJsonCounter))
    f.write('\nNumber of unique tokens: ' + str(len(frequencies)))
    indexSize = sys.getsizeof(frequencies) / 1000
    f.write("\nTotal size of index on disk: " + str(indexSize) + " KB")

if __name__ == '__main__':
    run()


