#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('./language-models')
sys.path.append('./data')
import random
from dataLoader import *

from unigramModel import *
from bigramModel import *
from trigramModel import *

from rhymeData import *

import pickle

# -----------------------------------------------------------------------------
# Core ------------------------------------------------------------------------
# Functions to implement: trainLyricsModels, selectNGramModel,
# generateSentence, and runLyricsGenerator

def trainLyricsModels(lyricsDirectory):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  loads lyrics data from the data/lyrics/<lyricsDirectory> folder
              using the pre-written DataLoader class, then creates an
              instance of each of the NGramModel child classes and trains
              them using the text loaded from the data loader. The list
              should be in tri-, then bi-, then unigramModel order.

              Returns the list of trained models.
    """

    dataLoader = DataLoader() # makes dataLoader an instance of the DataLoader class
    dataLoader.loadLyrics(lyricsDirectory)  # lyrics stored in dataLoader.lyrics

    # creates both regular and rhyming instances of each nGramModel
    # except for unigramModel, it only requires one instance because
    # the rhyming_model would be the same as the regular instance
    unigramModel = UnigramModel()
    bigramModel = BigramModel()
    rhyming_bigramModel = BigramModel()
    trigramModel = TrigramModel()
    rhyming_trigramModel = TrigramModel()

    # populates each nGramModel's dictionary
    unigramModel.trainModel(dataLoader.lyrics)
    bigramModel.trainModel(dataLoader.lyrics)
    rhyming_bigramModel.trainRhymingModel(dataLoader.lyrics)
    trigramModel.trainModel(dataLoader.lyrics)
    rhyming_trigramModel.trainRhymingModel(dataLoader.lyrics)

    # creates two lists containing each model in priority order
    models = [[trigramModel, bigramModel, unigramModel], [rhyming_trigramModel, rhyming_bigramModel, unigramModel]]

    return models

def selectNGramModel(models, sentence):
    """
    Requires: models is a list of NGramModel objects sorted by descending
              priority: tri-, then bi-, then unigrams.
    Modifies: nothing
    Effects:  starting from the beginning of the models list, returns the
              first possible model that can be used for the current sentence
              based on the n-grams that the models know. (Remember that you
              wrote a function that checks if a model can be used to pick a
              word for a sentence!)
    """

    # iterates through the list of models and returns the one that returns true
    for i in range(len(models)):
        if models[i].trainingDataHasNGram(sentence):
            return models[i]

def sentenceTooLong(desiredLength, currentLength):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  returns a bool indicating whether or not this sentence should
              be ended based on its length. This function has been done for
              you.
    """
    STDEV = 1
    val = random.gauss(currentLength, STDEV)
    return val > desiredLength

def generateSentence(models, desiredLength, sentence1=None):
    """
    Requires: models is a list of trained NGramModel objects sorted by
              descending priority: tri-, then bi-, then unigrams.
              desiredLength is the desired length of the sentence.
    Modifies: nothing
    Effects:  returns a list of strings where each string is a word in the
              generated sentence. The returned list should NOT include
              any of the special starting or ending symbols.

              For more details about generating a sentence using the
              NGramModels, see the spec.
    """

    # initializes sentence with starting symbols
    # then assigns the proper nGramModel to selected_model
    sentence = ['^::^', '^:::^']
    selected_model = selectNGramModel(models, sentence)

    # assigns functions to append/remove to avoid calling
    # dot operator in every loop, which enhances efficiency
    append = sentence.append
    remove = sentence.remove

    # this loop generates a sentence up to the final word
    i = 0
    while i <= desiredLength:
        next_word = selected_model.getNextToken(sentence)   # chooses and appends next_word based on
        append(next_word)                                   # selected nGramModel child class
        if i == 0:
            remove('^::^')   # removes symbol so it won't be counted in the line's length
        if i == 1:
            remove('^:::^')   # removes symbol so it won't be counted in the line's length
        if next_word == '$:::$':
            if len(sentence) > 2:   # prevents one word line since '$:::$' will be removed
                remove(next_word)
                if checkRhymableSentence(models, sentence):   # ensures subsequent lines can rhyme
                    if sentence1 is not None:                        # ensures that lines rhyme
                        if not checkForRhyme(sentence1, sentence):   # according to rhyme scheme
                            return sentence
                    else:
                        return sentence
                else:
                    try:    # if subsequent lines can't rhyme, tries to choose a rhymable word to end the line
                        selected_model = selectRhymingNGramModel(models, sentence)   # selects the nGramModel child
                        next_word = selected_model.getNextRhymable(sentence)         # class that can select a rhymable
                        append(next_word)                                            # word, then chooses the word
                        if sentence1 is not None:
                            if not checkForRhyme(sentence1, sentence):   # same as before
                                return sentence
                            else:
                                remove(next_word)   # if getNextRhymable chose a word that rhymes with an incorrect
                                i -= 1              # line according to the rhyme scheme, then removes that word
                                continue            # and goes back to the top (in hopes that next_word won't be
                        else:                       # '$:::$' again
                            return sentence
                    except IndexError or AttributeError:    # if there are no rhymable, next_word candidates, then
                        del sentence[:]                     # we scrap the whole line and start over (this almost
                        append('^::^')                      # never happens)
                        append('^:::^')
                        i = 0
                        continue
            else:
                del sentence[:]   # since the line is so short, and the symbols
                append('^::^')    # have been removed, we can't successfully call
                append('^:::^')   # getNextToken, see line 146
                i = 0
                continue
        if i == desiredLength - 1:   # catches line when it's one word from completion
            if checkRhymableSentence(models, sentence):           # performs the checkRhymableSentence sequence
                if sentence1 is not None:                         # (see line 138), except here, next_word isn't '$:::$'
                    if not checkForRhyme(sentence1, sentence):
                        return sentence
                    else:
                        remove(next_word)
                        i -= 1
                        continue
                else:
                    return sentence
            else:
                try:    # lines 192-204:  tries to complete the sentence with a rhymable word (see line 146)
                    selected_model = selectRhymingNGramModel(models, sentence)
                    next_word = selected_model.getNextRhymable(sentence)
                    append(next_word)
                    if sentence1 is not None:
                        if not checkForRhyme(sentence1, sentence):
                            return sentence
                        else:
                            remove(next_word)
                            i -= 1
                            continue
                    else:
                        return sentence
                except IndexError or AttributeError:    # if a rhymable word can't be chosen, removes the last
                        remove(sentence[-1])            # word on the line and returns to the top
                        i -= 1
                        continue
        selected_model = selectNGramModel(models, sentence)   # selects an nGramModel child class based on the
        i += 1                                                # new form of the current sentence and increments i

    return sentence

def printSongLyrics(verseOne, verseTwo, chorus):
    """
    Requires: verseOne, verseTwo, and chorus are lists of lists of strings
    Modifies: nothing
    Effects:  prints the song. This function is done for you.
    """

    verses = [verseOne, chorus, verseTwo, chorus]
    print('\n',)
    for verse in verses:
        for line in verse:
            print(' '.join(line)).capitalize()
        print('\n',)

def selectRhymingNGramModel(models, sentence1, sentence2=None):
    """
    Requires: models is a list of NGramModel objects sorted by descending
              priority: tri-, then bi-, then unigrams.
    Modifies: nothing
    Effects:  exactly the same as selectNGramModel, except with the constraint
              that the next word chosen must allow for subsequent lines to rhyme
    """

    # iterates through the list of models and returns the one that returns true
    for i in range(len(models)):
        if models[i].trainingDataHasRhymingNGram(sentence1, sentence2):
            return models[i]

def selectReverseNGramModel(models, sentence):
    """
    Requires: models is a list of NGramModel objects sorted by descending
              priority: tri-, then bi-, then unigrams.
    Modifies: nothing
    Effects:  exactly the same as the other selectNGramModel
              functions except calls trainingDataHasReverseNGram
              in order to correctly generate a sentence
              starting from the end
    """

    # iterates through the list of models and returns the one that returns true
    for i in range(len(models)):
        if models[i].trainingDataHasReverseNGram(sentence):
            return models[i]

def generateRhymingSentence(models, rhyme_scheme, sentence1, desiredLength, finalLine=False):
    """
    Requires: rhyme_scheme is a list of possible rhyme schemes,
              and sentences 1 & 2 are lists of strings.
    Modifies: nothing
    Effect:   does the same thing as generateSentence, except
              calls the rhyming functions so that the last
              word of sentence2 rhymes with the last word
              of sentence1
    """

    # initializes sentence with the ending symbol so that
    # sentence2 can be generated in reverse order
    sentence2 = ['$:::$']

    # assigns functions to remove/insert to avoid calling
    # dot operator in every loop, which enhances efficiency
    remove = sentence2.remove
    insert = sentence2.insert

    # selected model must be bigramModel
    # because sentence2 only contains one word
    selected_model = models[1]
    if not finalLine:
        next_word = selected_model.getNextRhymingToken(sentence1, sentence2)   # chooses a word that rhymes with the
        insert(0, next_word)                                                   # the last word of sentence1
        selected_model = selectReverseNGramModel(models, sentence2)   # now the sentence has 2 words, and a reversed
                                                                      # nGramModel child class can be chosen

    else:  # this prevents the last word in the last line of a stanza from ending in a conjunction
        next_word = selected_model.getNextRhymingToken(sentence1, sentence2, finalLine=True)
        insert(0, next_word)
        selected_model = selectReverseNGramModel(models, sentence2)

    # This loop generates a line in reverse order
    i = 0
    while i <= desiredLength:
        next_word = selected_model.getNextReverseToken(sentence2)   # chooses and appends next_word based on
        insert(0, next_word)                                        # the selected nGramModel child class
        if i == 1:            # once the sentence contains three
            remove('$:::$')   # strings, '$:::$' can be removed
        if next_word == '$:::$':
            if len(sentence2) > 2:   # prevents one word line since
                remove(next_word)    # '$:::$' will be removed
                if checkForRhyme(sentence1, sentence2):   # if sentence2 rhymes with
                    return sentence2                      # sentence1, returns sentence2
            else:
                remove(next_word)                                           # if '$:::$' was chosen as the second word,
                next_word = selected_model.getNextReverseToken(sentence2)   # removes it and selects and inserts a
                insert(0, next_word)                                        # different next_word, then returns to top
                i += 1
                continue
        if i == desiredLength - 1:   # catches line when it's one word from completion
            if checkForRhyme(sentence1, sentence2):   # see line 333
                if '$:::$' in sentence2:    # sometimes, for a reason we could not figure out,
                    remove('$:::$')         # '$:::$' would be in the middle of the line
                return sentence2
            else:
                remove(next_word)
                try:    # lines 367-373: tries to choose and insert the first word of sentence2
                    selected_model = selectNGramModel(models, sentence2)
                    next_word = selected_model.getNextReverseToken(sentence2)
                    insert(0, next_word)
                    i += 1
                    if '$:::$' in sentence2:
                        remove('$:::$')
                    return sentence2
                except IndexError or AttributeError:    # if a word can't be chosen, removes
                    remove(sentence2[0])                # the first word in sentence2, decrements
                    i -= 1                              # i, and returns to the top
                    continue
        selected_model = selectReverseNGramModel(models, sentence2)  # selects an nGramModel child class based on the
        i += 1                                                       # new form of the current sentence and increments i

    if '$:::$' in sentence2:    # prevents sentence2 from being returned containing '$:::$'
        remove('$:::$')

    return sentence2

def checkRhymableSentence(models, sentence):
    """
    Requires: sentence is a list of strings and rhymeLibrary
              is a txt file containing a pickle dictionary.
              see README for more info on rhymeLibrary
    Modifies: nothing
    Effects:  returns true if words that rhyme with the last word
              of sentence are in self.nGramCounts
    """

    # opens rhymeLibrary and loads the dictionary into rhyme_dict
    rhyme_library = open('rhymeLibrary.txt', 'r')
    rhyme_dict = pickle.load(rhyme_library)

    # assigns proper nGramModel class to selected_model
    selected_model = selectNGramModel(models, sentence)
    model_checker = selected_model.getDictionary()

    # see "Effects" section of docstring
    rhyming_list = rhyme_dict[sentence[-1]]
    for i in range(len(rhyming_list)):
        word = rhyming_list[i]
        if word in model_checker:
            return True

    return False

def checkForRhyme(sentence1, sentence2):
    """
    Requires: sentence1 and sentence 2 are lists of strings
              and rhymeLibrary is a txt file containing a
              pickle dictionary.
              see README for more info on rhymeLibrary
    Modifies: nothing
    Effects:  for creative part of reach. returns true if last words
              of sentence1 and sentence2 rhyme. this includes
              slant rhymes. will be called in generateRhymingSentence
              as a condition before a sentence is returned
    """

    # opens rhymeLibrary and loads the dictionary into rhyme_dict
    rhyme_library = open('rhymeLibrary.txt', 'r')
    rhyme_dict = pickle.load(rhyme_library)

    # See effects section of docstring
    rhyming_list = rhyme_dict[sentence1[-1]]
    for i in range(len(rhyming_list)):
        if sentence2[-1] in rhyming_list:
            return True

    return False

def chooseRhymeScheme(rhyme_schemes):
    """
    Requires: rhyme_schemes is a list of possible rhyme schemes
    Modifies: nothing
    Effects:  randomly selects a rhyme scheme that will
              be used in runLyricsGenerator to determine
              which sentences in a stanza will be assigned
              to sentence1 or sentence2
    """
    return random.choice(rhyme_schemes)

def runRhymingLyricsGenerator(models): #### REMOVE 0110 ###
    """
    Requires: models is a list of a trained nGramModel child class objects
    Modifies: nothing
    Effect:   exactly the same as runLyricsGenerator except that the verses
              and chorus will rhyme according to a randomly selected
              rhyme scheme
    """

    # selects rhyme scheme
    rhyme_scheme = chooseRhymeScheme(RHYME_SCHEMES)

    # creates verse/chorus lists
    verseOne = []
    verseTwo = []
    chorus = []

    # allows generateRhymingSentence to know which stanza
    # it is looking at in order to select sentence1
    stanzas = [verseOne, verseTwo, chorus]

    # assigns functions to append1,2,c to avoid calling
    # dot operator in every loop, which enhances efficiency
    append1 = verseOne.append
    append2 = verseTwo.append
    append_c = chorus.append
    append = [append1, append2, append_c]

    # constant values for desiredLength and stanza_length
    desiredLength = 6
    stanza_length = 4

    # generates each verse and chorus according to rhyme_scheme
    for i in range(len(append)):
        line = 0   # will be used to determine the line to be rhymed with (rhyme-reference line)
        for j in range(stanza_length):
            if len(stanzas[i]) < stanza_length:   # ensures that a fifth line isn't generated
                if len(stanzas[i]) == 0:
                    model = models[0]   # selects non-rhyming models
                    new_line = generateSentence(model, desiredLength)   # assigns a generated sentence to new_line,
                    append[i](new_line)                                 # appends it to the current stanza, and then
                    new_line = []                                       # empties new_line to be repopulated
                elif rhyme_scheme[j] == rhyme_scheme[j - 1]:   # for '0011' rhyme scheme
                    while len(stanzas[i]) < stanza_length:
                        sentence1 = stanzas[i][line]    # indicates the rhyme-reference line
                        model = models[1]               # and then selects rhyming models
                        try:
                            new_line = generateRhymingSentence(model, rhyme_scheme, sentence1, desiredLength)
                            append[i](new_line)
                            new_line = []
                        except IndexError:      # if, for some reason, a rhyming sentence cannot be generated, then
                            model = models[0]   # goes ahead and generates a regular line, giving the stanza variety
                            new_line = generateSentence(model, desiredLength)
                            append[i](new_line)
                            new_line = []
                        if len(stanzas[i]) < stanza_length - 1:   # ensures that a fifth line isn't generated
                            model = models[0]
                            new_line = generateSentence(model, desiredLength, sentence1)
                            append[i](new_line)
                            new_line = []
                        if rhyme_scheme[0] != rhyme_scheme[-1]:   # maintains '0011'
                            line = 2
                        else:   # sets rhyme-reference line for '0110'
                            line = 0
                elif (j == 2):
                    if rhyme_scheme[j] == rhyme_scheme[j - 2]:   # for '0101' rhyme scheme
                        while len(stanzas[i]) < stanza_length - 1:
                            sentence1 = stanzas[i][line]   # see lines 452-453
                            model = models[1]
                            try:
                                new_line = generateRhymingSentence(model, rhyme_scheme, sentence1, desiredLength)
                                append[i](new_line)
                                new_line = []
                                line = 1
                            except IndexError:   # see lines 458-459
                                model = models[0]
                                new_line = generateSentence(model, desiredLength)
                                append[i](new_line)
                                new_line = []
                                line = 1
                else:   # for second line of '0110' or '0101' rhyme scheme
                    sentence1 = stanzas[i][line]
                    model = models[0]
                    new_line = generateSentence(model, desiredLength, sentence1)   # second line doesn't need to rhyme
                    append[i](new_line)
                    new_line = []
                    line = 1

    return printSongLyrics(verseOne, verseTwo, chorus)


# -----------------------------------------------------------------------------
# Reach -----------------------------------------------------------------------
# Functions to implement: trainMusicModels, generateMusicalSentence, and
# runMusicGenerator

def trainMusicModels(musicDirectory):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  works exactly as trainLyricsModels from the core, except
              now the dataLoader calls the DataLoader's loadMusic() function
              and takes a music directory name instead of an artist name.
              Returns a list of trained models in order of tri-, then bi-, then
              unigramModel objects.
    """

    dataLoader = DataLoader() # makes dataLoader an instance of the DataLoader class
    dataLoader.loadMusic(musicDirectory)  # music stored in dataLoader.songs

    # creates instances of each nGramModel child class
    unigramModel = UnigramModel()
    bigramModel = BigramModel()
    trigramModel = TrigramModel()

    # populates each nGramModel's dictionary
    unigramModel.trainModel(dataLoader.songs)
    bigramModel.trainModel(dataLoader.songs)
    trigramModel.trainModel(dataLoader.songs)

    # creates a list containing each model in priority order
    models = [trigramModel, bigramModel, unigramModel]

    return models

def generateMusicalSentence(models, desiredLength, possiblePitches):
    """
    Requires: possiblePitches is a list of pitches for a musical key
    Modifies: nothing
    Effects:  works exactly like generateSentence from the core, except
              now we call the NGramModel child class' getNextNote()
              function instead of getNextToken(). Everything else
              should be exactly the same as the core.
    """

    # initializes sentence with the ending symbol so that
    # sentence2 can be generated in reverse order
    sentence = ['^::^', '^:::^']
    selected_model = selectNGramModel(models, sentence)

    # assigns functions to remove/insert to avoid calling
    # dot operator in every loop, which enhances efficiency
    append = sentence.append
    remove = sentence.remove

    # This loop generates a musical sentence
    for i in range(desiredLength):
        next_note = selected_model.getNextNote(sentence, possiblePitches)
        append(next_note)
        if i == 0:
            remove('^::^')
        if i == 1:
            remove('^:::^')
        if next_note == '$:::$':
            if '^:::^' in sentence:
                remove('^:::^')
                continue
            else:
                remove('$:::$')
                return sentence
        elif sentenceTooLong(desiredLength, len(sentence)):
            if '^:::^' in sentence:
                continue
            return sentence
        selected_model = selectNGramModel(models, sentence)

    return sentence

# -----------------------------------------------------------------------------
# Main ------------------------------------------------------------------------

def getUserInput(teamName, lyricsSource, musicSource):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  prints a welcome menu for the music generator and prints the
              options for the generator. Loops while the user does not input
              a valid option. When the user selects 1, 2, or 3, returns
              that choice.

              Note: this function is for the reach only. It is done for you.
    """
    print('Welcome to the', teamName, 'music generator!\n')
    prompt = 'Here are the menu options:\n' + \
             '(1) Generate song lyrics by ' + lyricsSource + '\n' \
             '(2) Generate a song using data from ' + musicSource + '\n' \
             '(3) Quit the music generator\n'

    userInput = -1
    while userInput < 1 or userInput > 3:
        print(prompt)
        userInput = input('Please enter a choice between 1 and 3: ')
        try:
            userInput = int(userInput)
        except ValueError:
            userInput = -1

    return userInput

def main():
    """
    Requires: nothing
    Modifies: nothing
    Effects:  this is your main function, which is done for you. It runs the
              entire generator program for both the reach and the core.
              It begins by loading the lyrics and music data, then asks the
              user to input a choice to generate either lyrics or music.

              Note that for the core, only choice 1 (the lyrics generating
              choice) needs to be completed; if the user inputs 2, you
              can just have the runMusicGenerator function print "Under
              construction."

              Also note that you can change the values of the first five
              variables based on your team's name, artist name, etc.
    """
    program_name = 'Lyricist AI'
    lyricsSource = 'Coldplay' #eliminate, make it work for everything
    lyricsDirectory = 'Coldplay'

    print('Starting program and loading data...')
    lyricsModels = trainLyricsModels(lyricsDirectory)
    print('Data successfully loaded\n')

    userInput = getUserInput(program_name, lyricsSource)

    while userInput != 2:
        print('\n',)
        if userInput == 1:
            print('Your song will be ready shortly!')
            print("And it's going to rhyme too!\n")
            runRhymingLyricsGenerator(lyricsModels)

        print('\n',)
        userInput = getUserInput(program_name, lyricsSource)

    print('\nThank you for using the ', program_name, '!')



if __name__ == '__main__':
    main()
    unigramModel = UnigramModel()
    bigramModel = BigramModel()
    trigramModel = TrigramModel()




