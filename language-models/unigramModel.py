import random
from nGramModel import *


# -----------------------------------------------------------------------------
# UnigramModel class ----------------------------------------------------------
# Core functions to implement: trainModel, trainingDataHasNGram, and
# getCandidateDictionary

class UnigramModel(NGramModel):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the UnigramModel object)
        Effects:  this is the UnigramModel constructor, which is done
                  for you. It allows UnigramModel to access the data
                  in the NGramModel class by calling the NGramModel
                  constructor.
        """
        super(UnigramModel, self).__init__()

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts
        Effects:  this function populates the self.nGramCounts dictionary,
                  which is a dictionary of {string: integer} pairs.
                  For further explanation of UnigramModel's version of
                  self.nGramCounts, see the spec.

                  Note: make sure to use the return value of prepData to
                  populate the dictionary, which will allow the special
                  symbols to be included as their own tokens in
                  self.nGramCounts. For more details, see the spec.
        """
        return

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the UnigramModel, see the spec.
        """
        return False

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNgGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  UnigramModel sees as candidates, see the spec.
        """
        return {}



# -----------------------------------------------------------------------------
# Testing code ----------------------------------------------------------------

if __name__ == '__main__':
    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    sentence = [ 'brown' ]
    unigramModel = UnigramModel()
    # add your own testing code here if you like


