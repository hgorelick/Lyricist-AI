#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
from dataLoader import *
import rhymeApi
from requests.exceptions import ConnectionError
import copy

# both lists will not return any rhymes. dealt with in fixIt(word)
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

    dataLoader = DataLoader() # makes dataLoader an instance of the DataLoader class
    dataLoader.loadLyrics(LyricsDirectory)  # lyrics stored in dataLoader.

    # makes text_copy a copy of list text
    text_copy = copy.deepcopy(dataLoader.lyrics)

    # makes rhyme_dict an empty dictionary
    rhyme_dict = {}

    # assigns update function to update to avoid calling
    # dot operator in every loop, which enhances efficiency
    update = rhyme_dict.update

    # opens rhymeLibrary.txt to be written
    file_name = open('rhymeLibrary.txt', 'wb')

    # loops through text_copy. every word in text_copy
    # is created as a key in rhyme_dict. each keys' value
    # is a list of words that rhyme with that key
    for i in range(len(text_copy)):
        print(i)
        for j in range(len(text_copy[i])):
            word = text_copy[i][j]
            if word in rhyme_dict:
                continue
            elif checkWordNeedsFixing(word):
                try:
                    rhyme_list = rhymeApi.api(fixIt(word))
                    update({word: rhyme_list})
                except ConnectionError:
                    pickle.dump(rhyme_dict, file_name)
                    file_name.close()
                    print(i)
                    exit(1)
            else:
                try:
                    rhyme_list = rhymeApi.api(word)
                    update({word: rhyme_list})
                except ConnectionError:
                    pickle.dump(rhyme_dict, file_name)
                    file_name.close()
                    print(i)
                    exit(1)

    # writes rhyme_dict to rhymeLibrary.txt then closes the file
    pickle.dump(rhyme_dict, file_name)
    file_name.close()

def fixIt(word):
    """
    Requires: word is a string in either list
              contractions or exceptions
    Modifies: fixed
    Effects:  rhymeApi.api() will return an empty list
              if any of these words are used as the input.
              therefore, this function returns fixed, which
              is a word that can be used as a substitute word
              in rhymeApi.api()
    """
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
    """
    Requires: word is a string
    Modifies: nothing
    Effects:  returns true if and only if word is
              in contractions or exceptions
    """
    if word in contractions:
        return True
    if word in exceptions:
        return True
    return False

if __name__ == '__main__':
    libraryWriter('Coldplay')
