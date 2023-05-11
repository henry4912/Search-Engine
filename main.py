import os
from bs4 import BeautifulSoup
import json
import re
from nltk.stem import PorterStemmer


def run():
    porterStem = PorterStemmer()
    validJsonCounter = 0  # valid json files
    # validURL = [] #list of valid urls (the url in the json file)
    invalidJsonCounter = 0  # invalid json files
    frequencies = {}  # token frequencies
    badURL = []  # invalid json files
    # testingLimit = 0 #amount of json files to test
    assignmentFolder = os.getcwd() + '\ANALYST'
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
                    if key == 'content':
                        soup = BeautifulSoup(value, 'html.parser')
                        tokens = tokenizer(soup.text)
                        for t in tokens:
                            t = porterStem.stem(t)
                            if not is_stopword(t):
                                if t in frequencies.keys():
                                    if currURL in frequencies[t].keys():
                                        frequencies[t][currURL] += 1
                                    else:
                                        # frequencies[t] = {}
                                        frequencies[t][currURL] = 1
                                else:
                                    frequencies[t] = {}
                                    frequencies[t][currURL] = 1

    f = open("fixedJSONOutput.txt", "w+")
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

    f.write('\nFrequencies Length: ' + str(len(frequencies)))

    f.write('\n\n\n\nFrequencies Dictionary: ')
    for keys, values in frequencies.items():
        f.write('token: ' + str(keys))
        f.write('\ntoken URL count: ' + str(len(values)) + '\n')
        for key, value in values.items():
            f.write('%s       %s' % (key, value))
            f.write('\n')

    # print(frequencies)


def tokenizer(contents):
    tokens = re.findall(r'[a-z0-9]+', contents.lower())
    return tokens


def is_stopword(token):
    stopWords = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'aren\'t',
                 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by',
                 'can\'t', 'cannot', 'could', 'couldn\'t', 'did', 'didn\'t', 'do', 'does', 'doesn\'t', 'doing',
                 'don\'t',
                 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadn\'t', 'has', 'hasn\'t', 'have',
                 'haven\'t', 'having', 'he', 'he\'d', 'he\'ll', 'he\'s', 'her', 'here', 'here\'s', 'hers', 'herself',
                 'him', 'himself', 'his', 'how', 'how\'s', 'i', 'i\'d', 'i\'ll', 'i\'m', 'i\'ve', 'if', 'in', 'into',
                 'is', 'isn\'t', 'it', 'it\'s', 'its', 'itself', 'let\'s', 'me', 'more', 'most', 'mustn\'t', 'my',
                 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours',
                 'ourselves', 'out', 'over', 'own', 'same', 'shan\'t', 'she', 'she\'d', 'she\'ll', 'she\'s', 'should',
                 'shouldn\'t', 'so', 'some', 'such', 'than', 'that', 'that\'s', 'the', 'their', 'theirs', 'them',
                 'themselves', 'then', 'there', 'there\'s', 'these', 'they', 'they\'d', 'they\'ll', 'they\'re',
                 'they\'ve',
                 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'wasn\'t', 'we',
                 'we\'d',
                 'we\'ll', 'we\'re', 'we\'ve', 'were', 'weren\'t', 'what', 'what\'s', 'when', 'when\'s', 'where',
                 'where\'s',
                 'which', 'while', 'who', 'who\'s', 'whom', 'why', 'why\'s', 'with', 'won\'t', 'would', 'wouldn\'t',
                 'you',
                 'you\'d', 'you\'ll', 'you\'re', 'you\'ve', 'your', 'yours', 'yourself', 'yourselves']

    if token in stopWords:
        return True
    else:
        return False


run()


