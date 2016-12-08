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

# -----------------------------------------------------------------------------
# Core ------------------------------------------------------------------------
# Functions to implement: trainLyricsModels, selectNGramModel,
# generateSentence, and runLyricsGenerator
''' test'''

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
    dataLoader.loadLyrics(lyricsDirectory) # lyrics stored in dataLoader.lyrics

    # Creates instances of each nGramModel
    unigramModel = UnigramModel()
    bigramModel = BigramModel()
    trigramModel = TrigramModel()

    # Populates each nGramModel's dictionary
    unigramModel.trainModel(dataLoader.lyrics)
    bigramModel.trainModel(dataLoader.lyrics)
    trigramModel.trainModel(dataLoader.lyrics)

    # Creates a list containing each model in priority order
    models = [trigramModel, bigramModel, unigramModel]

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

def generateSentence(models, desiredLength):
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

    # This loop first chooses and adds a next_word
    # based on the current sentence and
    # selected_model, then it checks if the
    # sentence contains any symbols and
    # removes them if necessary before
    # returning the completed sentence
    for i in range(desiredLength):
        next_word = selected_model.getNextToken(sentence)
        append(next_word)
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

    pysynth.make_wav(song, fn=songName)



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
            runLyricsGenerator(lyricsModels)
        elif userInput == 2:
            songName = raw_input('What would you like to name your song? ')
            runMusicGenerator(musicModels, 'wav/' + songName + '.wav')

        print '\n',
        userInput = getUserInput(teamName, lyricsSource, musicSource)

    print '\nThank you for using the', teamName, 'music generator!'



if __name__ == '__main__':
    #main()
    #unigramModel = UnigramModel()
    #bigramModel = BigramModel()
    #trigramModel = TrigramModel()
    print runLyricsGenerator(trainLyricsModels('Coldplay'))
    #print trainMusicModels('gamecube')
    #print runMusicGenerator(trainMusicModels('gamecube'), 'Test')



