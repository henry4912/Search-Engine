import os,sys
from bs4 import BeautifulSoup
import json
import re
from nltk.stem import PorterStemmer

def run():
    porterStem = PorterStemmer()
    idCounter = 1
    docID = {}
    validJsonCounter = 0  # valid json files
    # validURL = [] #list of valid urls (the url in the json file)
    invalidJsonCounter = 0  # invalid json files
    frequencies = {}  # token frequencies
    badURL = []  # invalid json files
    # testingLimit = 0 #amount of json files to test
    assignmentFolder = os.getcwd() + '/ANALYST'
    # print(assignmentFolder)
    for directories in os.listdir(assignmentFolder):
        # print(directories)
        subfolder = os.path.join(assignmentFolder, directories)
        # while testingLimit < 10:
        for file in os.listdir(os.path.join(assignmentFolder, directories)):
            # print(os.path.join(assignmentFolder, directories))
            # print(os.path.join(subfolder, file))
            s = os.path.join(subfolder, file)
            with open(os.path.join(subfolder, file), 'r') as j:
                # testingLimit = testingLimit + 1
                jsonContentDictionary = json.load(j)
                currURL = ''
                for key, value in jsonContentDictionary.items():
                    if key == 'url':
                        currURL = value
                        validJsonCounter = validJsonCounter + 1
                        docID[currURL] = idCounter
                    if key == 'content':
                        soup = BeautifulSoup(value, 'xml')
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

    f = open("fixedJSONOutput.txt", "w+")

    f.write('\nNumber of documents: ' + str(idCounter))
    f.write('\nNumber of unique tokens: ' + str(len(frequencies)))
    indexSize = sys.getsizeof(frequencies) / 1000
    f.write("\nTotal size of index on disk: " + str(indexSize) + "KB")

    f.write('valid json: ' + str(validJsonCounter) + '\n')
    f.write('invalid json: ' + str(invalidJsonCounter))
    f.write('\nEvery bad json file: \n')

    for link in badURL:
        f.write(link)
        f.write('\n')
    """
    f.write('\nEvery valid URL: \n')


    for link in validURL:
        f.write(link)
        f.write('\n')
    """
  
    f.write('\n\n\n\nFrequencies Dictionary:\n')
    for keys, values in frequencies.items():
        f.write('token: ' + str(keys))
        f.write('\ntoken URL count: ' + str(len(values)) + '\n')
        # for key, value in values.items():
        #    f.write('%s       %s' % (key, value))
        #    f.write('\n')

    # print(frequencies)

   



def tokenizer(contents):
    tokens = re.findall(r'[a-z0-9]+', contents.lower())
    return tokens

if __name__ == '__main__':
    run()


