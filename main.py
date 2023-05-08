import os
from bs4 import BeautifulSoup


def run():
    assignmentFolder = os.getcwd() + '\ANALYST'
    # print(assignmentFolder)
    for directories in os.listdir(assignmentFolder):
        # print(directories)
        subfolder = os.path.join(assignmentFolder, directories)
        for file in os.listdir(os.path.join(assignmentFolder, directories)):
            # print(os.path.join(assignmentFolder, directories))
            print(os.path.join(subfolder, file))
            with open(os.path.join(subfolder, file), 'r') as json:
                soup = BeautifulSoup(json, 'lxml')
                print(soup.contents)
            break
        break


run()