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

        # Assigns copy of dictionary candidates to cumulative
        cumulative = copy.deepcopy(candidates)

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

    def prepRhymingData(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: nothing
        Effects:  exact same as prepData except leaves out
                  '^::^' and '^:::^' because they are not
                  needed to produce a sentence in reverse order.
                  furthermore, sandwiches each sublist with the
                  '$:::$' symbol in order to maintain
                  same ending sentence conditions
        """

        # makes text_copy a copy of list text
        text_copy = copy.deepcopy(text)

        # iterates through textCopy and inserts/appends symbols
        for i in range(len(text_copy)):
            text_copy[i].insert(0, '$:::$')
            text_copy[i].append('$:::$')

        return text_copy

    def trainRhymingModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts
        Effects:  this function populates the self.nGramCounts dictionary.
                  It does not need to be modified here because you will
                  override it in the NGramModel child classes according
                  to the spec.
        """
        return

    def trainingDataHasRhymingNGram(self, sentence1, sentence2=None):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 2
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next rhyming token for the sentence.
        """
        return False

    def trainingDataHasReverseNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 2
        Modifies: nothing
        Effects:  exactly the same trainingDataHasReverseNGram.
                  must be in all nGramModel child classes
        """
        return False


    def getRhymingCandidateDictionary(self, sentence1, sentence2, finalLine=False):
        """
        Requires: same as getCandidateDictionary
        Modifies: nothing
        Effects:  same as getCandidateDictionary except the
                  the candidate words will rhyme with the last word
                  of the compared sentence.
        """
        return {}

    def getReverseCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 2
        Modifies: nothing
        Effects:  exactly the same getCandidateDictionary.
                  must be in all nGramModel child classes
        """
        return {}

    def getRhymables(self, sentence):
        """
            Requires: sentence is a list of strings
            Modifies: nothing
            Effects:  same as getRhymingCandidateDictionary
                      except that it is only used for the last
                      word of the first line of a verse or chorus
        """
        return {}

    def getDictionary(self):
        """
        Requires: nothing
        Modifies: nothing
        Effects:  returns already trained nGramCounts
                  to be used in checkRhymableSentence
        """
        return {}

    def getNextRhymingToken(self, sentence1, sentence2):
        """
        Requires: same as getNextToken
        Modifies: nothing
        Effects:  this function operates exactly like getNextToken,
                  except that it is only used for the last word of a
                  sentence and calls getRhymingCandidateDictionary instead
                  of getCandidateDictionary. it will return a word that makes
                  sentence rhyme with the compared sentence
        """
        return self.weightedChoice(self.getRhymingCandidateDictionary(sentence1, sentence2))

    def getNextReverseToken(self, sentence):
        """
        Requires: same as getNextToken
        Modifies: nothing
        Effects:  this function operates like the other NextToken functions
                  except that it is used to generate a sentence in reverse order
        """
        return self.weightedChoice(self.getReverseCandidateDictionary(sentence))

    def getNextRhymable(self, sentence):
        """
        Requires: same as getNextToken
        Modifies: nothing
        Effects:  this function operates exactly like getNextRhymingToken,
                  except that it is only used for the last word of the first
                  line of a verse or chorus
        """
        return self.weightedChoice(self.getRhymables(sentence))


# -----------------------------------------------------------------------------
# Testing code ----------------------------------------------------------------

if __name__ == '__main__':
    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    choices = { 'the': 2, 'quick': 1, 'brown': 1 }
    sentence = ['brown']
    nGramModel = NGramModel()
    print(nGramModel.prepData(text))
    print(nGramModel.weightedChoice(choices))
    print(nGramModel.getNextToken(sentence))




