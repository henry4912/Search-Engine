# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 13:27:59 2023

@author: Henry
"""

import json
import re
from nltk.stem import PorterStemmer
from tkinter import *
import main

# https://stackoverflow.com/questions/7945182/opening-multiple-an-unspecified-number-of-files-at-once-and-ensuring-they-are
def search():
    
    index = getFinalIndex('final-index.json')
    docID = getDocID('docID.json')
    
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
    
    '''
    f = open('reportM2.txt', 'w+')
    f.write('Student Names: Derrick Jones, Sabrina Yang, Henry Ha, Christine Nguyen\n')
    f.write('Student IDs: 93547582, 27422353, 25602171, 56965805\n\n')
    f.write('Report M2:\n\n')
    f.close()
    '''
    
    def clicked():
        results = findResults(searchBox.get().lower(), index, docID)
        #reportWriteM2(searchBox.get(), results)
        labelResults.configure(text=results)   
    
    search = Button(frame2, text='Search', command=clicked)
    search.pack(side='left')
    frame2.place(relx=0.5, rely=0.25, anchor=N)

    window.mainloop()
    

def findResults(text, index, docID):
    sets = []
    results = ''
    porterStem = PorterStemmer()
    tokens = text.split()
    tokens = [porterStem.stem(t) for t in tokens]
    
    for token in tokens:
        if token not in index.keys():
            return 'No results found'
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
        return 'No results found'
    elif len(intersection) > 5:
        for url in intersection[:5]:
            results += str(url) + '\n\n'
    else:
        for url in urlFreq:
            results += str(url) + '\n\n'
    
    return results

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