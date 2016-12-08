import random
from nGramModel import *
from collections import Counter
import copy


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

        # Makes a copy of text, then passes it through prepData
        unigram_text = copy.deepcopy(text)
        unigram_text = self.prepData(unigram_text)

        # Prevents symbols from being counted
        exclude = {'^::^', '^:::^'}

        # Uses Counter function with a list comprehension
        # to make a dictionary of each word and its count
        self.nGramCounts = Counter(word for sublist in unigram_text
                                   for word in sublist if word not in exclude)

        return self.nGramCounts

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the UnigramModel, see the spec.
        """

        # Checks if self.nGramCounts is an empty dictionary
        # then returns true or false based on condition
        if self.nGramCounts != {}:
            return True
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
        return self.nGramCounts



# -----------------------------------------------------------------------------
# Testing code ----------------------------------------------------------------

if __name__ == '__main__':
    text = [ ['the', 'quick', 'brown', 'fox'], ['jumps', 'over'], ['the', 'lazy', 'dog'] ]
    sentence = [ 'brown' ]
    unigramModel = UnigramModel()
    print unigramModel.trainModel(text)
    print unigramModel.trainingDataHasNGram(sentence)
    print unigramModel.getCandidateDictionary(sentence)



