#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('./language-models')
sys.path.append('./data')
sys.path.append('./pysynth')
import pysynth
import random
from dataLoader import *

from unigramModel import *
from bigramModel import *
from trigramModel import *

from musicData import *
from rhymeData import *

import cPickle as pickle

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
    dataLoader = DataLoader()
    dataLoader.loadLyrics(lyricsDirectory)  # lyrics stored in dataLoader.lyrics

    # creates both regular and rhyming
    # instances of each nGramModel
    # except for unigramModel, it
    # only requires one instance because
    # the rhyming_model would be the same
    # as the regular instance
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

    # Iterates through the list of models
    # and returns the one that returns to true
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

    # Initializes sentence with starting symbols
    # then assigns the proper nGramModel
    # to selected_model
    sentence = ['^::^', '^:::^']
    selected_model = selectNGramModel(models, sentence)

    # Assigns functions to append/remove to avoid
    # calling dot operator in every loop
    # which enhances efficiency
    append = sentence.append
    remove = sentence.remove

    # this word
    ignore = 'instrumental'

    # This loop generates a sentence
    # up to the final word, then it checks if the
    # sentence contains any symbols, if so
    # it removes them, then, if the sentence
    # is supposedly completed, it checks if
    # a subsequent sentence can rhyme with it,
    # if so, then it returns the completed sentence
    i = 0
    while i <= desiredLength:
        next_word = selected_model.getNextToken(sentence)
        append(next_word)
        if i == 0:
            remove('^::^')
        if i == 1:
            remove('^:::^')
        if next_word == '$:::$':
            if len(sentence) > 2:
                remove(next_word)
                if checkRhymableSentence(models, sentence):
                    if sentence1 is not None:
                        if not checkForRhyme(sentence1, sentence):
                            return sentence
                    else:
                        return sentence
                else:
                    try:
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
                    except IndexError or AttributeError:
                        del sentence[:]
                        append('^::^')
                        append('^:::^')
                        i = 0
                        continue
            else:
                try:
                    remove(next_word)
                    next_word = selected_model.getNextToken(sentence)
                    append(next_word)
                    continue
                except IndexError or AttributeError:
                    del sentence[:]
                    append('^::^')
                    append('^:::^')
                    i = 0
                    continue
        elif sentenceTooLong(desiredLength, len(sentence)):
            if checkRhymableSentence(models, sentence):
                if sentence1 is not None:
                    if not checkForRhyme(sentence1, sentence):
                        return sentence
                    else:
                        remove(next_word)
                        i -= 1
                        continue
                else:
                    return sentence
            else:
                remove(sentence[-1])
                compare = selected_model.getNextToken(sentence)
                if compare == next_word:
                    remove(sentence[-1])
                    continue
        if i == desiredLength - 1:
            if checkRhymableSentence(models, sentence):
                if sentence1 is not None:
                    if not checkForRhyme(sentence1, sentence):
                        return sentence
                    else:
                        remove(next_word)
                        i -= 1
                        continue
                else:
                    return sentence
            else:
                try:
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
                except IndexError or AttributeError:
                    if i == desiredLength - 1:
                        remove(sentence[-1])
                        i -= 1
                        continue
                    else:
                        compare = selected_model.getNextToken(sentence)
                        if compare == next_word:
                            remove(sentence[-1])
                            i -= 1
                            continue
        selected_model = selectNGramModel(models, sentence)
        i += 1

    return sentence

def printSongLyrics(verseOne, verseTwo, chorus):
    """
    Requires: verseOne, verseTwo, and chorus are lists of lists of strings
    Modifies: nothing
    Effects:  prints the song. This function is done for you.
    """

    verses = [verseOne, chorus, verseTwo, chorus]
    print '\n',
    for verse in verses:
        for line in verse:
            print (' '.join(line)).capitalize()
        print '\n',

def runLyricsGenerator(models):
    """
    Requires: models is a list of a trained nGramModel child class objects
    Modifies: nothing
    Effects:  generates a verse one, a verse two, and a chorus, then
              calls printSongLyrics to print the song out.
    """

    # Creates verse/chorus lists
    verseOne = []
    verseTwo = []
    chorus = []

    # Assigns functions to each append to avoid
    # calling dot operator in every loop
    # which enhances efficiency
    append1 = verseOne.append
    append2 = verseTwo.append
    append_c = chorus.append
    append = [append1, append2, append_c]

    # Generates each verse and chorus
    for i in range(len(append)):
        for j in range(4):
            new_line = generateSentence(models, 7)
            append[i](new_line)
            new_line = []

    return printSongLyrics(verseOne, verseTwo, chorus)

def selectRhymingNGramModel(models, sentence1, sentence2=None):
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

    # Iterates through the list of models
    # and returns the one that returns to true
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

    # Iterates through the list of models
    # and returns the one that returns to true
    for i in range(len(models)):
        if models[i].trainingDataHasReverseNGram(sentence):
            return models[i]

def generateRhymingSentence(models, rhyme_scheme, sentence1, desiredLength):
    """
    Requires: rhyme_scheme is a list of possible rhyme schemes,
              and sentences 1 & 2 are lists of strings.
    Modifies: nothing
    Effect:   does the same thing as generateSentence, except
              calls the rhyming functions so that the last
              word of sentence2 rhymes with the last word
              of sentence1
    """
    # Initializes sentence with the ending symbol
    # so that sentence2 can be generated in
    # reverse order
    sentence2 = ['$:::$']

    # Assigns functions to remove/insert to avoid
    # calling dot operator in every loop
    # which enhances efficiency
    remove = sentence2.remove
    insert = sentence2.insert

    selected_model = models[1]###
    try:
        next_word = selected_model.getNextRhymingToken(sentence1, sentence2)
        insert(0, next_word)
        selected_model = selectReverseNGramModel(models, sentence2)
    except IndexError:
        next_word = selected_model.getNextRhymingToken(sentence1, sentence2)
        insert(0, next_word)
        selected_model = selectReverseNGramModel(models, sentence2)

    # This loop first chooses and adds a next_word
    # based on the current sentence and
    # selected_model, then it checks if the
    # sentence contains any symbols and
    # removes them if necessary before
    # returning the completed sentence
    for i in range(desiredLength):
        next_word = selected_model.getNextReverseToken(sentence2)
        insert(0, next_word)
        if i == 1:
            remove('$:::$')
        if next_word == '$:::$':
            if len(sentence2) > 2:
                remove(next_word)
                if checkForRhyme(sentence1, sentence2):
                    if '$:::$' in sentence2:
                        remove('$:::$')
                    return sentence2
            else:
                remove(next_word)
                next_word = selected_model.getNextReverseToken(sentence2)
                insert(0, next_word)
                continue
        elif sentenceTooLong(desiredLength, len(sentence2)):
            if checkForRhyme(sentence1, sentence2):
                if '$:::$' in sentence2:
                    remove('$:::$')
                return sentence2
            else:
                remove(next_word)
                try:
                    selected_model = selectRhymingNGramModel(models, sentence2)
                    next_word = selected_model.getNextRhymingToken(sentence1, sentence2)
                    insert(0, next_word)
                    if '$:::$' in sentence2:
                        remove('$:::$')
                    return sentence2
                except IndexError or AttributeError:
                    remove(sentence2[0])
                    i -= 1
                    continue
        if i == desiredLength - 1:
            if checkForRhyme(sentence1, sentence2):
                if '$:::$' in sentence2:
                    remove('$:::$')
                return sentence2
            else:
                remove(next_word)
                try:
                    selected_model = selectRhymingNGramModel(models, sentence1, sentence2)
                    next_word = selected_model.getNextRhymingToken(sentence1, sentence2)
                    insert(0, next_word)
                    if '$:::$' in sentence2:
                        remove('$:::$')
                    return sentence2
                except IndexError or AttributeError:
                    remove(sentence[0])
                    i -= 1
                    continue

        selected_model = selectNGramModel(models, sentence2)

    if '$:::$' in sentence2:
        remove('$:::$')

    return sentence2

def checkRhymableSentence(models, sentence):
    """
    Requires: sentence is a list of strings
    Modifies: nothing
    Effects:  returns true if words that rhyme with the last word
              of sentence are in self.nGramCounts
    """

    rhyme_library = open(
        r'Creative_AI_31_Repository\data\rhymeLibrary.txt',
        'rb')
    rhyme_dict = pickle.load(rhyme_library)

    # Assigns proper nGramModel class to selected_model
    selected_model = selectNGramModel(models, sentence)
    model_checker = selected_model.getDictionary()

    # See effects section of docstring
    rhyming_list = rhyme_dict[sentence[-1]]
    for i in range(len(rhyming_list)):
        word = rhyming_list[i]
        if word in model_checker:
            return True

    return False

def checkForRhyme(sentence1, sentence2):
    """
    Requires: sentence1 and sentence 2 are lists of strings
    Modifies: nothing
    Effects: for creative part of reach. returns true if last words
             of sentence1 and sentence2 rhyme. this includes
             slant rhymes. will be called in generateRhymingSentence
             as a condition before a sentence is returned
    """

    rhyme_library = open(
        r'Creative_AI_31_Repository\data\rhymeLibrary.txt',
        'rb')
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

def runRhymingLyricsGenerator(models):
    """
    Requires: models is a list of a trained nGramModel child class objects
    Modifies: nothing
    Effect:   exactly the same as runLyricsGenerator except that the verses
              and chorus will rhyme according to a randomly selected
              rhyme scheme
    """

    # Selects rhyme scheme
    rhyme_scheme = chooseRhymeScheme(RHYME_SCHEMES)

    # Creates verse/chorus lists
    verseOne = []
    verseTwo = []
    chorus = []

    # Allows generateRhymingSentence to know
    # which stanza it is looking at in order
    # to select sentence1
    stanzas = [verseOne, verseTwo, chorus]

    # Assigns functions to each append to avoid
    # calling dot operator in every loop
    # which enhances efficiency
    append1 = verseOne.append
    append2 = verseTwo.append
    append_c = chorus.append
    append = [append1, append2, append_c]

    desiredLength = 6
    stanza_length = 4

    # Generates each verse and chorus
    # according to rhyme_scheme
    for i in range(len(append)):
        line = 0
        for j in range(stanza_length):
            if len(stanzas[i]) < stanza_length:
                if len(stanzas[i]) == 0:
                    model = models[0]
                    new_line = generateSentence(model, desiredLength)
                    append[i](new_line)
                    new_line = []
                elif rhyme_scheme[j] == rhyme_scheme[j - 1]:
                    while len(stanzas[i]) < stanza_length:
                        sentence1 = stanzas[i][line]
                        model = models[1]
                        try:
                            new_line = generateRhymingSentence(model, rhyme_scheme, sentence1, desiredLength)
                            append[i](new_line)
                            new_line = []
                        except IndexError:
                            model = models[0]
                            new_line = generateSentence(model, desiredLength)
                            append[i](new_line)
                            new_line = []
                        if len(stanzas[i]) < stanza_length - 1:
                            model = models[0]
                            new_line = generateSentence(model, desiredLength, sentence1)
                            append[i](new_line)
                            new_line = []
                        if rhyme_scheme[0] != rhyme_scheme[-1]:
                            line = 2
                        else:
                            line = 0
                elif (j == 2):
                    if rhyme_scheme[j] == rhyme_scheme[j - 2]:
                        while len(stanzas[i]) < stanza_length - 1:
                            sentence1 = stanzas[i][line]
                            model = models[1]
                            new_line = generateRhymingSentence(model, rhyme_scheme, sentence1, desiredLength)
                            append[i](new_line)
                            new_line = []
                            line = 1
                else:
                    sentence1 = stanzas[i][line]
                    model = models[0]
                    new_line = generateSentence(model, desiredLength, sentence1)
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
    dataLoader = DataLoader()
    dataLoader.loadMusic(musicDirectory)  # music stored in dataLoader.songs

    # Creates instances of each nGramModel
    unigramModel = UnigramModel()
    bigramModel = BigramModel()
    trigramModel = TrigramModel()

    # Populates each nGramModel's dictionary
    unigramModel.trainModel(dataLoader.songs)
    bigramModel.trainModel(dataLoader.songs)
    trigramModel.trainModel(dataLoader.songs)

    # Creates a list containing each model in priority order
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

    # Initializes sentence with starting symbols
    # then assigns the proper nGramModel
    # to selected_model
    sentence = ['^::^', '^:::^']
    selected_model = selectNGramModel(models, sentence)

    # Assigns functions to append/remove to avoid
    # calling dot operator in every loop
    # which enhances efficiency
    append = sentence.append
    remove = sentence.remove

    # This loop first chooses and adds a next_word
    # based on the current sentence and
    # selected_model, then it checks if the
    # sentence contains any symbols and
    # removes them if necessary before
    # returning the completed sentence
    for i in range(desiredLength):
        next_note = selected_model.getNextNote(sentence, possiblePitches)
        append(next_note)
        if i == 0:
            remove('^::^')
        if i == 1:
            remove('^:::^')
        if sentence[-1] == '$:::$':
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

def runMusicGenerator(models, songName):
    """
    Requires: models is a list of trained models
    Modifies: nothing
    Effects:  runs the music generator as following the details in the spec.

              Note: For the core, this should print "Under construction".
    """
    key_signature = random.choice(KEY_SIGNATURES.values())

    song = generateMusicalSentence(models, 60, key_signature)

    return pysynth.make_wav(song, fn=songName)




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
    print 'Welcome to the', teamName, 'music generator!\n'
    prompt = 'Here are the menu options:\n' + \
             '(1) Generate song lyrics by ' + lyricsSource + '\n' \
             '(2) Generate a song using data from ' + musicSource + '\n' \
             '(3) Quit the music generator\n'

    userInput = -1
    while userInput < 1 or userInput > 3:
        print prompt
        userInput = raw_input('Please enter a choice between 1 and 3: ')
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
    teamName = 'Coldplay Creative AI'
    lyricsSource = 'Coldplay'
    musicSource = 'Nintendo Gamecube'
    lyricsDirectory = 'Coldplay'
    musicDirectory = 'gamecube'

    print 'Starting program and loading data...'
    lyricsModels = trainLyricsModels(lyricsDirectory)
    musicModels = trainMusicModels(musicDirectory)
    print 'Data successfully loaded\n'

    userInput = getUserInput(teamName, lyricsSource, musicSource)

    while userInput != 3:
        print '\n',
        if userInput == 1:
            runRhymingLyricsGenerator(lyricsModels)
        elif userInput == 2:
            songName = raw_input('What would you like to name your song? ')
            runMusicGenerator(musicModels, 'wav/' + songName + '.wav')

        print '\n',
        userInput = getUserInput(teamName, lyricsSource, musicSource)

    print '\nThank you for using the', teamName, 'music generator!'



if __name__ == '__main__':
    main()
    #test_sentence = ['you', 'cant', 'hurt', 'me']
    unigramModel = UnigramModel()
    bigramModel = BigramModel()
    trigramModel = TrigramModel()
    #trainLyricsModels('Coldplay')
    #runRhymingLyricsGenerator(trainLyricsModels('Coldplay'))
    #print trainMusicModels('gamecube')
    #print runMusicGenerator(trainMusicModels('gamecube'), 'Test')
   # print pronouncing.rhymes("yellow")



