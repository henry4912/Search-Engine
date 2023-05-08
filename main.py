import os
from bs4 import BeautifulSoup

def run():
    assignmentFile =  os.getcwd() + '/DEV'
    for directories in os.listdir(assignmentFile):
        for file in os.path.join(assignmentFile, directories):
            with open(os.path.join(assignmentFile, file), 'r') as json:
                soup = BeautifulSoup(json, 'lxml')
                print(soup.contents)
            break
        break