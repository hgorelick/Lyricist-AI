#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cPickle as pickle
from dataLoader import *
import rhymeApi
from requests.exceptions import ConnectionError
import copy

contractions = ['wont', 'dont', 'cant', 'wouldnt', 'shouldnt',
                'couldnt', 'hasnt', 'havent']
exceptions = ['oooon', 'oooo', 'oooooo', 'oh', 'ohoh', 'ooooooooh', 'oooohooohoooohoh',
              'youooooooooooh', 'lalalalalalalalaiy', 'ahahahahahahahah']
def libraryWriter(LyricsDirectory):
    """
    What it does: loops through ever word in the Coldplay
                  lyrics directory, creates a rhyme list,
                  then writes that rhyme list and corresponding
                  word to rhymeLibrary.txt
    """
    dataLoader = DataLoader()
    dataLoader.loadLyrics(LyricsDirectory)  # lyrics stored in dataLoader.

    # makes copy of list text
    textCopy = copy.deepcopy(dataLoader.lyrics)

    rhyme_dict = {}
    update = rhyme_dict.update
    file_name = open('rhymeLibrary.txt', 'wb')
    for i in range(len(textCopy)):
        print i
        for j in range(len(textCopy[i])):
            word = textCopy[i][j]
            if word in rhyme_dict:
                continue
            elif checkWordNeedsFixing(word):
                try:
                    rhyme_list = rhymeApi.api(fixIt(word))
                    update({word: rhyme_list})
                except ConnectionError:
                    pickle.dump(rhyme_dict, file_name)
                    file_name.close()
                    print i
                    exit(1)
            else:
                try:
                    rhyme_list = rhymeApi.api(word)
                    update({word: rhyme_list})
                except ConnectionError:
                    pickle.dump(rhyme_dict, file_name)
                    file_name.close()
                    print i
                    exit(1)
    pickle.dump(rhyme_dict, file_name)
    file_name.close()
        #i += 1
    #file = open('rhymeLibrary.txt', 'r+')
    #file.write(rhyme_dict)
    #file.close()

def fixIt(word):
    if word in contractions:
        if word == (contractions[0] or contractions[1]):
            fixed = 'note'
            return fixed
        elif word == contractions[2]:
            fixed = 'ant'
            return fixed
        elif word == (contractions[3] or contractions[4] or contractions[5]):
            fixed = 'dent'
            return fixed
        elif word == contractions[6]:
            fixed = 'accent'
            return fixed
        elif word == contractions[7]:
            fixed = 'patent'
            return fixed
    elif word in exceptions:
        if word == exceptions[0]:
            fixed = word[-2:]
            return fixed
        elif word == (exceptions[1] or exceptions[2]):
            fixed = 'new'
            return fixed
        elif word == (exceptions[3] or exceptions[4] or exceptions[5] or exceptions[6]):
            fixed = 'oh'
            return fixed
        elif word == exceptions[-2]:
            fixed = word[:3]
            return fixed
        elif word == exceptions[-3]:
            fixed = 'lie'
            return fixed
        elif word == exceptions[-1]:
            fixed = 'ah'
            return fixed

def checkWordNeedsFixing(word):
    if word in contractions:
        return True
    if word in exceptions:
        return True
    return False

if __name__ == '__main__':
    libraryWriter('Coldplay')
