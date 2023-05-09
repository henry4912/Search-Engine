import os
from bs4 import BeautifulSoup
import json
import re


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


def tokenizer(contents):
    tokens = re.findall(r'[a-z0-9]+', contents)
    return tokens


run()