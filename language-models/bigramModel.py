import random
from nGramModel import *
import copy
import cPickle as pickle

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

        # makes a copy of text, then passes it through prepData
        bigram_text = copy.deepcopy(text)
        bigram_text = self.prepData(bigram_text)

        # updates self.nGramCounts with known key value pairs
        self.nGramCounts.update({'^::^': {'^:::^': len(bigram_text)}})

        # prevents symbols from being counted again
        exclude = {'^::^', '^:::^'}

        # assigns update function to update to avoid calling
        # dot operator in every loop, which enhances efficiency
        update = self.nGramCounts.update

        # updates self.nGramCounts with bigram frequencies
        bigram_count = 1
        for i in range(len(bigram_text)):
            for j in range(len(bigram_text[i]) - 1):
                word1 = bigram_text[i][j]       # makes words 1/2 a two-word sequence (a bigram) in text.
                word2 = bigram_text[i][j + 1]   # loop ensures that every two-word sequence is checked
                if word1 and word2 not in exclude:
                    if word1 in self.nGramCounts:
                        if word2 in self.nGramCounts[word1]:
                            self.nGramCounts[word1][word2] += 1   # changes only an existing bigram's value
                        else:   # adds a new second word to an existing unigram
                            self.nGramCounts[word1].update({word2: bigram_count + 1})
                    else:   # adds a brand new bigram
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

        # checks for the last word of sentence is a key in self.nGramCounts
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

        # creates empty candidates dictionary
        candidates = {}

        # checks last word of the sentence. if that word exists
        # as a key in self.nGramCounts then updates dictionary
        # candidates with that key's value
        if sentence[-1] in self.nGramCounts:
            candidates.update(self.nGramCounts[sentence[-1]])

        return candidates

    def trainRhymingModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts, a two-dimensional dictionary.
        Effects:  this function behaves exactly as trainModel
                  except that it puts all text in reverse order first.

                  this will allow for a rhyming sentence to be
                  generated starting with the last word and
                  going backwards.
        """

        # makes bigram_text a copy of text, then passes it through prepRhymingData
        bigram_text = copy.deepcopy(text)
        bigram_text = self.prepRhymingData(bigram_text)

        # symbols shouldn't be counted because they won't
        # be needed to produce sentence in reverse order
        exclude = {'^::^', '^:::^'}

        # assigns update function to update to avoid calling
        # dot operator in every loop, which enhances efficiency
        update = self.nGramCounts.update

        bigram_count = 1
        for i in range(len(bigram_text)):   # updates self.nGramCounts with bigram frequencies exactly
            j = len(bigram_text[i]) - 1     # like trainModel (see lines 55-67), except in reverse
            while j > 0:
                word1 = bigram_text[i][j]
                word2 = bigram_text[i][j - 1]
                if word1 and word2 not in exclude:
                    if word1 in self.nGramCounts:
                        if word2 in self.nGramCounts[word1]:
                            self.nGramCounts[word1][word2] += 1
                        else:
                            self.nGramCounts[word1].update({word2: bigram_count + 1})
                    else:
                        update({word1: {word2: bigram_count}})
                j -= 1

        return self.nGramCounts

    def trainingDataHasRhymingNGram(self, sentence1, sentence2=None):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 2
                  and rhymeLibrary is a txt file containing a pickle dictionary.
                  see README for more info on rhymeLibrary
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next rhyming token for the sentence.
        """

        # opens rhymeLibrary and loads the dictionary into rhyme_dict
        rhyme_library = open('rhymeLibrary.txt', 'r')
        rhyme_dict = pickle.load(rhyme_library)

        # checks if self.nGramCounts contains words that rhyme
        # with the last word of sentence if so, returns true
        if sentence2 is None:
            rhyming_list = rhyme_dict[sentence1[-1]]
            for i in range(len(rhyming_list)):
                word = rhyming_list[i]
                if word in self.nGramCounts[sentence1[-1]]:
                    return True
        # checks the same conditions as above, except that
        # it uses sentence1 as the rhyme-reference line
        else:
            keys = self.nGramCounts[sentence2[-1]]
            rhyming_list = rhyme_dict[sentence2[-1]]
            compare_list = rhyme_dict[sentence1[-1]]
            for i in range(len(rhyming_list)):
                word = rhyming_list[i]
                if (word in keys) and (word in compare_list):
                    return True

        return False

    def trainingDataHasReverseNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 2
        Modifies: nothing
        Effects:  exactly the same as trainingDataHasNGram.
                  must exist in each nGramModel child class
        """

        # checks for the first word of sentence is a key in self.nGramCounts
        if sentence[1] in self.nGramCounts.keys():
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

        # makes constrainedCandidates an empty dictionary
        constrainedCandidates = {}

        # assigns update function to update to avoid calling
        # dot operator in every loop, which enhances efficiency
        update = constrainedCandidates.update

        # checks if any of the words in allCandidates
        # rhyme with the last word in sentence1.
        # if so, updates constrainedCandidates with
        # that key value pair
        rhyming_list = rhyme_dict[sentence1[-1]]
        for i in range(len(rhyming_list)):
            word = rhyming_list[i]
            if word in allCandidates:
                update({word: allCandidates[word]})

        return constrainedCandidates

    def getReverseCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  exact same as getCandidateDictionary.
                  must exist in ever nGramModel child class
        """

        # creates empty candidates dictionary
        candidates = {}

        # checks first word of the sentence. if that
        # word exists as a key in self.nGramCounts
        # then updates dictionary candidates with that
        # key's value
        if sentence[0] in self.nGramCounts:
            candidates.update(self.nGramCounts[sentence[0]])

        return candidates

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
                if word in self.nGramCounts:
                    if '$:::$' in self.nGramCounts[word]:        # ensures that a rhyming word can
                        update({word: allCandidates[keys[i]]})   # be chosen in subsequent lines

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
    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    text.append([ 'quick', 'brown' ])
    text.append(['mother', 'mary', 'comes', 'to', 'me'])
    text.append(['let', 'it', 'be'])
    text.append(['it', 'is'])
    text.append(['it', 'will'])
    text.append(['it', 'might'])
    sentence = [ 'lazy', 'quick', 'brown', 'dog' ]
    sentenceA = ['mother', 'mary', 'comes', 'to', 'me']
    sentenceB = ['let', 'it']
    bigramModel = BigramModel()
    print bigramModel.trainModel(text)
    print bigramModel.trainingDataHasNGram(sentence)
    print bigramModel.getCandidateDictionary(sentence)
    print bigramModel.getRhymingCandidateDictionary(sentenceA, sentenceB)


