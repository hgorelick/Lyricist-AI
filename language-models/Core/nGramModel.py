import random
import sys
sys.path.append('../data')
from musicData import *
import copy



# -----------------------------------------------------------------------------
# NGramModel class ------------------------------------------------------------
# Core functions to implement: prepData, weightedChoice, and getNextToken
# Reach functions to implement: getNextNote

class NGramModel(object):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the NGramModel object)
        Effects:  This is the NGramModel constructor. It sets up an empty
                  dictionary as a member variable. It is called from the
                  constructors of the NGramModel child classes. This
                  function is done for you.
        """
        self.nGramCounts = {}

    def __str__(self):
        """
        Requires: nothing
        Modifies: nothing
        Effects:  returns the string to print when you call print on an
                  NGramModel object. This function is done for you.
        """
        return 'This is an NGramModel object'

    def prepData(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: nothing
        Effects:  returns a copy of text where each inner list starts with
                  the symbols '^::^' and '^:::^', and ends with the symbol
                  '$:::$'. For example, if an inner list in text were
                  ['hello', 'goodbye'], that list would become
                  ['^::^', '^:::^', 'hello', 'goodbye', '$:::$'] in the
                  returned copy.

                  Make sure you are not modifying the original text
                  parameter in this function.
        """

        # Makes copy of list text
        textCopy = copy.deepcopy(text)

        # iterates through textCopy and inserts/appends symbols
        for i in range(len(textCopy)):
            textCopy[i].insert(0, '^:::^')
            textCopy[i].insert(0, '^::^')
            textCopy[i].append('$:::$')

        return textCopy



    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts
        Effects:  this function populates the self.nGramCounts dictionary.
                  It does not need to be modified here because you will
                  override it in the NGramModel child classes according
                  to the spec.
        """
        return

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns a bool indicating whether or not this n-gram model
                  can be used to choose the next token for the current
                  sentence. This function does not need to be modified because
                  you will override it in NGramModel child classes according
                  to the spec.
        """
        return False

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. This function does not need to be
                  modified because you will override it in the NGramModel child
                  classes according to the spec.
        """
        return {}

    def weightedChoice(self, candidates):
        """
        Requires: candidates is a dictionary; the keys of candidates are items
                  you want to choose from and the values are integers
        Modifies: nothing
        Effects:  returns a candidate item (a key in the candidates dictionary)
                  based on the algorithm described in the spec.
        """

        # Prevents symbols from being included in cumulative
        exclude = {'^::^', '^:::^'}

        # Assigns copy of dictionary candidates to cumulative
        cumulative = {word: candidates[word] for word in candidates if word not in exclude}

        # Creates list of cumulative's keys
        keys = cumulative.keys()

        # Updates cumulatives' cumulative values
        if len(cumulative) > 1:
            i = 1
            while i in range(len(cumulative)):
                cumulative[keys[i]] = cumulative[keys[i]] + cumulative[keys[i - 1]]
                i += 1

        # Used for assinging a random int to x
        values = cumulative.values()

        # Assigns random int in range min(values) - max(values) to x
        if len(cumulative) > 1:
            x = random.randrange(min(values), max(values))
        else:
            x = values[0]

        # Iterates through cumulative's values
        # comparing each to x, then returns
        # first key with a value greater than x
        for i in range(len(cumulative)):
            if x <= cumulative[keys[i]]:
                return keys[i]

    def getNextToken(self, sentence):
        """
        Requires: sentence is a list of strings, and this model can be used to
                  choose the next token for the current sentence
        Modifies: nothing
        Effects:  returns the next token to be added to sentence by calling
                  the getCandidateDictionary and weightedChoice functions.
                  For more information on how to put all these functions
                  together, see the spec.
        """
        return self.weightedChoice(self.getCandidateDictionary(sentence))

    def getNextNote(self, musicalSentence, possiblePitches):
        """
        Requires: musicalSentence is a list of PySynth tuples,
                  possiblePitches is a list of possible pitches for this
                  line of music (in other words, a key signature), and this
                  model can be used to choose the next note for the current
                  musical sentence
        Modifies: nothing
        Effects:  returns the next note to be added to the "musical sentence".
                  For details on how to do this and how this will differ
                  from the getNextToken function from the core, see the spec.

                  Please note that this function is for the reach only.
        """
        allCandidates = self.getCandidateDictionary(musicalSentence)

        constrainedCandidates = {}

        # Prevents symbols from being counted
        exclude = {'^::^', '^:::^', '$:::$'}

        keys = allCandidates.keys()

        filtered_keys = []
        append = filtered_keys.append

        for i in range(len(keys)):
            if keys[i] not in exclude:
                if keys[i][0][1] == ('b' or '#'):
                    if len(keys[i][0]) > 2:
                        append(keys[i][0][:-1])
                    else:
                        append(keys[i])
                elif len(keys[i][0]) > 1:
                    append(keys[i][0][:-1])
                else:
                    append(keys[i][0])
            elif keys[i] == '$:::$':
                append(keys[i])

        values = allCandidates.values()

        update = constrainedCandidates.update

        for i in range(len(filtered_keys)):
            if filtered_keys[i] in possiblePitches:
                update({keys[i]: values[i]})
            if keys[i] == '$':
                update({keys[i]: values[i]})

        if constrainedCandidates != {}:
            return self.weightedChoice(constrainedCandidates)
        else:
            next_note = random.choice(possiblePitches) + '4'
            note_duration = random.choice(NOTE_DURATIONS)
            return next_note, note_duration



# -----------------------------------------------------------------------------
# Testing code ----------------------------------------------------------------

if __name__ == '__main__':
    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    choices = { 'the': 2, 'quick': 1, 'brown': 1 }
    sentence = ['brown']
    nGramModel = NGramModel()
    print nGramModel.prepData(text)
    print nGramModel.weightedChoice(choices)
    print nGramModel.getNextToken(sentence)
    print nGramModel.getNextNote()





