import os
from bs4 import BeautifulSoup
import json
import re

"""
def run():
    counter = 0
    frequencies = {}

    assignmentFolder = os.getcwd() + '\ANALYST'
    # print(assignmentFolder)
    for directories in os.listdir(assignmentFolder):
        # print(directories)
        subfolder = os.path.join(assignmentFolder, directories)
        for file in os.listdir(os.path.join(assignmentFolder, directories)):
            # print(os.path.join(assignmentFolder, directories))
            # print(os.path.join(subfolder, file))
            with open(os.path.join(subfolder, file), 'r') as j:
                soup = BeautifulSoup(j, 'lxml')
                jsonContents = json.loads(soup.text)
                currURL = jsonContents['url']
                tokens = tokenizer(jsonContents['content'])
                # print(jsonContents['content'])
                for t in tokens:
                    if t in frequencies.keys():
                        if currURL in frequencies[t].keys():
                            frequencies[t][currURL] += 1
                        else:
                            frequencies[t] = {}
                            frequencies[t][currURL] = 1
                    else:
                        frequencies[t] = {}
                        frequencies[t][currURL] = 1

            counter += 1
            print(counter)
"""

def run():
    validJsonCounter = 0 #valid json files
    #validURL = [] #list of valid urls (the url in the json file)
    invalidJsonCounter = 0 #invalid json files
    frequencies = {} #token frequencies
    badURL = [] #invalid json files
    #testingLimit = 0 #amount of json files to test
    assignmentFolder = os.getcwd() + '\ANALYST'
    # print(assignmentFolder)
    for directories in os.listdir(assignmentFolder):
        # print(directories)
        subfolder = os.path.join(assignmentFolder, directories)
        #while testingLimit < 10:
        for file in os.listdir(os.path.join(assignmentFolder, directories)):
            #print(os.path.join(assignmentFolder, directories))
            #print(os.path.join(subfolder, file))
            s = os.path.join(subfolder, file)
            with open(os.path.join(subfolder, file), 'r') as j:
                    #testingLimit = testingLimit + 1
                    jsonContentDictionary = json.load(j)
                    currURL = ''
                    for key, value in jsonContentDictionary.items():
                        if key == 'url':
                            currURL = value
                            validJsonCounter = validJsonCounter + 1
                        if key == 'content':
                            tokens = tokenizer(value)
                            for t in tokens:
                                if t in frequencies.keys():
                                    if currURL in frequencies[t].keys():
                                        frequencies[t][currURL] += 1
                                    else:
                                        #frequencies[t] = {}
                                        frequencies[t][currURL] = 1
                                else:
                                    frequencies[t] = {}
                                    frequencies[t][currURL] = 1
                        

                        
    

    f = open("fixedJSONOutput.txt", "w")        
    f.write('valid json: ' + str(validJsonCounter) +'\n')
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
    
    f.write('\nFrequencies Length: ' + str(len(frequencies)))
    
    f.write('\n\n\n\nFrequencies Dictionary: ')
    for keys, values in frequencies.items():
        f.write('token: ' + str(keys))
        f.write('\ntoken URL count: '+str(len(values)) + '\n')
        for key, value in values.items():
            f.write('%s       %s' % (key, value))
            f.write('\n')
 

def tokenizer(contents):
    tokens = re.findall(r'[a-z0-9]+', contents)
    return tokens


run()