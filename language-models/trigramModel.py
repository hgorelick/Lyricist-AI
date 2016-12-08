import random
from nGramModel import *
import copy


# -----------------------------------------------------------------------------
# TrigramModel class ----------------------------------------------------------
# Core functions to implement: trainModel, trainingDataHasNGram, and
# getCandidateDictionary

class TrigramModel(NGramModel):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the NGramModel object)
        Effects:  this is the TrigramModel constructor, which is done
                  for you. It allows TrigramModel to access the data
                  from the NGramModel class.
        """
        super(TrigramModel, self).__init__()

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts, a three-dimensional dictionary. For
                  examples and pictures of the TrigramModel's version of
                  self.nGramCounts, see the spec.
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries as values,
                  where those inner dictionaries have strings as keys
                  and dictionaries of {string: integer} pairs as values.

                  Note: make sure to use the return value of prepData to
                  populate the dictionary, which will allow the special
                  symbols to be included as their own tokens in
                  self.nGramCounts. For more details, see the spec.
        """

        # Makes a copy of text, then passes it through prepData
        trigram_text = copy.deepcopy(text)
        trigram_text = self.prepData(trigram_text)

        # Counts frequency of each trigram in text_copy
        # then updates the self.nGramCounts dictionary
        # as specified by the spec
        trigram_count = 1
        for i in range(len(trigram_text)):
            for j in range(len(trigram_text[i]) - 2):
                word1 = trigram_text[i][j]
                word2 = trigram_text[i][j + 1]
                word3 = trigram_text[i][j + 2]
                if word1 in self.nGramCounts:
                    if word2 in self.nGramCounts[word1]:
                        if word3 in self.nGramCounts[word1][word2]:
                            self.nGramCounts[word1][word2][word3] += 1
                        else:
                            self.nGramCounts[word1][word2].update({word3: trigram_count + 1})
                    else:
                        self.nGramCounts[word1].update({word2: {word3: trigram_count + 1}})
                else:
                    self.nGramCounts.update({word1: {word2: {word3: trigram_count + 1}}})

        return self.nGramCounts

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 2
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the TrigramModel, see the spec.
        """

        # Checks if the sentence's second to last
        # word is a key in self.nGramCounts, and
        # if it is, checks if the last word in the
        # sentence is also a key in self.nGramCounts,
        # if so, returns true
        if sentence[-2] in self.nGramCounts.keys():
            if sentence[-1] in self.nGramCounts[sentence[-2]].keys():
                return True
        return False

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  TrigramModel sees as candidates, see the spec.
        """

        # Creates empty candidates dictionary
        candidates = {}

        # Checks checks the second to last
        # and last words of the sentence.
        # If that word exists as a key in self.nGramCounts
        # then updates dictionary candidates with that
        # key's value
        if sentence[-2] in self.nGramCounts:
            if sentence[-1] in self.nGramCounts[sentence[-2]]:
                candidates.update(self.nGramCounts[sentence[-2]][sentence[-1]])

        return candidates


# -----------------------------------------------------------------------------
# Testing code ----------------------------------------------------------------

if __name__ == '__main__':
    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    sentence = [ 'the', 'quick', 'brown' ]
    trigramModel = TrigramModel()
    print trigramModel.trainModel(text)
    print trigramModel.trainingDataHasNGram(sentence)
    print trigramModel.getCandidateDictionary(sentence)

