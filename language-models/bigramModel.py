import random
from nGramModel import *
import copy


# -----------------------------------------------------------------------------
# BigramModel class -----------------------------------------------------------
# Core functions to implement: trainModel, trainingDataHasNGram, and
# getCandidateDictionary

class BigramModel(NGramModel):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the BigramModel object)
        Effects:  this is the BigramModel constructor, which is done
                  for you. It allows BigramModel to access the data
                  from the NGramModel class by calling the NGramModel
                  constructor.
        """
        super(BigramModel, self).__init__()

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts, a two-dimensional dictionary. For examples
                  and pictures of the BigramModel's version of
                  self.nGramCounts, see the spec.
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries of
                  {string: integer} pairs as values.

                  Note: make sure to use the return value of prepData to
                  populate the dictionary, which will allow the special
                  symbols to be included as their own tokens in
                  self.nGramCounts. For more details, see the spec.
        """

        # Makes a copy of text, then passes it through prepData
        bigram_text = copy.deepcopy(text)
        bigram_text = self.prepData(bigram_text)

        # Updates self.nGramCounts with known key value pairs
        self.nGramCounts.update({'^::^': {'^:::^': len(bigram_text)}})

        # Prevents symbols from being counted again
        exclude = {'^::^', '^:::^'}

        # Helps optimize for loop
        update = self.nGramCounts.update

        # Counts frequency of each bigram in text_copy
        # then updates the self.nGramCounts dictionary
        # as specified by the spec
        bigram_count = 1
        for i in range(len(bigram_text)):
            for j in range(len(bigram_text[i]) - 1):
                word1 = bigram_text[i][j]
                word2 = bigram_text[i][j + 1]
                if word1 and word2 not in exclude:
                    if word1 in self.nGramCounts:
                        if word2 in self.nGramCounts[word1]:
                            self.nGramCounts[word1][word2] += 1
                        else:
                            self.nGramCounts[word1].update({word2: bigram_count + 1})
                    else:
                        update({word1: {word2: bigram_count + 1}})

        return self.nGramCounts

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 1
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the BigramModel, see the spec.
        """

        # Checks for the last element of sentence in keys
        if sentence[-1] in self.nGramCounts.keys():
            return True
        return False

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  BigramModel sees as candidates, see the spec.
        """

        # Creates empty candidates dictionary
        candidates = {}

        # Checks every word in sentence up to the last.
        # If that word exists as a key in self.nGramCounts
        # then updates dictionary candidates with that
        # key's value
        if sentence[-1] in self.nGramCounts:
            candidates.update(self.nGramCounts[sentence[-1]])

        return candidates


# -----------------------------------------------------------------------------
# Testing code ----------------------------------------------------------------

if __name__ == '__main__':
    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    text.append([ 'quick', 'brown' ])
    sentence = [ 'lazy', 'quick', 'brown', 'dog' ]
    bigramModel = BigramModel()
    print bigramModel.trainModel(text)
    print bigramModel.trainingDataHasNGram(sentence)
    print bigramModel.getCandidateDictionary(sentence)


