import random
from nGramModel import *
from collections import Counter
import copy
import cPickle as pickle

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

    def trainingDataHasNGram(self, sentence1):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the UnigramModel, see the spec.
        """

        # checks if self.nGramCounts is an empty dictionary
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

    def trainingDataHasRhymingNGram(self, sentence1, sentence2=None):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  exactly the same as trainingDataHasNGram.
                  must exist in each nGramModel child class
        """

        # checks if self.nGramCounts is an empty dictionary
        # then returns true or false based on condition
        if self.nGramCounts != {}:
            return True
        return False

    def trainingDataHasReverseNGram(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  exactly the same as trainingDataHasNGram.
                  must exist in each nGramModel child class
        """

        # checks if self.nGramCounts is an empty dictionary
        # then returns true or false based on condition
        if self.nGramCounts != {}:
            return True
        return False

    def getRhymingCandidateDictionary(self, sentence1, sentence2, finalLine=False):
        """
        Requires: same as getCandidateDictionary and rhymeLibrary
                  is a txt file containing a pickle dictionary.
                  see README for more info on rhymeLibrary
        Modifies: nothing
        Effects:  same as getCandidateDictionary except the
                  the candidate words will rhyme with the last word
                  of the compared sentence.
        """

        # opens rhymeLibrary and loads the dictionary into rhyme_dict
        rhyme_library = open('rhymeLibrary.txt', 'r')
        rhyme_dict = pickle.load(rhyme_library)

        # makes allCandidates the returned dictionary of getCandidateDictionary
        allCandidates = self.getCandidateDictionary(sentence2)

        # filters out '$:::$', it can't rhyme so shouldn't be included
        exclude = '$:::$'
        if exclude in allCandidates:
            del allCandidates[exclude]

        # if generating the final line of a stanza,
        # makes sure the last word isn't one of these
        if finalLine:
            bad_endings = [
                'for', 'nor', 'and', 'but', 'or', 'although', 'as', 'if',
                'because', 'than', 'that', 'unless', 'until', 'til', 'when',
                'where', 'whether', 'which', 'while', 'who', 'both', 'such', 'rather'
            ]
            for i in range(len(bad_endings)):
                if bad_endings[i] in allCandidates:
                    del allCandidates[bad_endings[i]]

        keys = allCandidates.keys()

        # makes constrainedCandidates an empty dictionary
        constrainedCandidates = {}

        # assigns update function to update to avoid calling
        # dot operator in every loop, which enhances efficiency
        update = constrainedCandidates.update

        # checks if any of the words in allCandidates
        # rhymes with the last word in sentence1.
        # if so, updates constrainedCandidates with
        # that key value pair
        for i in range(len(keys)):
            rhyming_list = rhyme_dict[keys[i]]
            for j in range(len(rhyming_list)):
                word = rhyming_list[j]
                if word in self.getDictionary():
                    update({word: allCandidates[keys[i]]})

        return constrainedCandidates

    def getReverseCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNgGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  exactly the same as getCandidateDictionary.
                  must exist in each nGramModel child class
        """
        return self.nGramCounts

    def getRhymables(self, sentence):
        """
        Requires: sentence is a list of strings and rhymeLibrary
                  is a txt file containing a pickle dictionary.
                  see README for more info on rhymeLibrary
        Modifies: nothing
        Effects:  only used for the last word of
                  sentence in generateSentence. ensures
                  that it will be possible for the rest
                  of the sentences in the verse or the
                  chorus can rhyme
        """

        # opens rhymeLibrary and loads the dictionary into rhyme_dict
        rhyme_library = open('rhymeLibrary.txt', 'r')
        rhyme_dict = pickle.load(rhyme_library)

        # makes allCandidates the returned dictionary of getCandidateDictionary
        allCandidates = self.getCandidateDictionary(sentence)

        # filters out '$:::$', it can't rhyme so shouldn't be included
        exclude = '$:::$'
        if exclude in allCandidates:
            del allCandidates[exclude]

        # makes constrainedCandidates an empty dictionary
        constrainedCandidates = {}

        # assigns update function to update to avoid calling
        # dot operator in every loop, which enhances efficiency
        update = constrainedCandidates.update

        # checks if any of the words in allCandidates
        # rhymes with the last word in sentence1.
        # if so, updates constrainedCandidates with
        # that key value pair
        rhyming_list = rhyme_dict[sentence[-1]]
        for i in range(len(rhyming_list)):
            word = rhyming_list[i]
            if word in allCandidates:
                update({word: allCandidates[word]})

        return constrainedCandidates

    def getDictionary(self):
        """
        Requires: nothing
        Modifies: nothing
        Effects:  returns already trained nGramCounts
                  to be used in checkRhymableSentence
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



