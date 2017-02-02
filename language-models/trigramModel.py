import random
from nGramModel import *
import copy
import cPickle as pickle

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

        # makes a copy of text, then passes it through prepData
        trigram_text = copy.deepcopy(text)
        trigram_text = self.prepData(trigram_text)

        # updates self.nGramCounts with trigram frequencies
        trigram_count = 1
        for i in range(len(trigram_text)):
            for j in range(len(trigram_text[i]) - 2):
                word1 = trigram_text[i][j]       # makes words 1-3 a three-word sequence (a trigram) in text.
                word2 = trigram_text[i][j + 1]   # loop ensures that every three-word sequence is checked
                word3 = trigram_text[i][j + 2]
                if word1 in self.nGramCounts:
                    if word2 in self.nGramCounts[word1]:
                        if word3 in self.nGramCounts[word1][word2]:
                            self.nGramCounts[word1][word2][word3] += 1   # changes only an existing trigram's value
                        else:   # adds a new third word to an existing bigram
                            self.nGramCounts[word1][word2].update({word3: trigram_count + 1})
                    else:   # adds a new bigram to an existing unigram
                        self.nGramCounts[word1].update({word2: {word3: trigram_count + 1}})
                else:   # adds a brand new trigram
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

        # checks if the sentence's second to last word is a key
        # in self.nGramCounts, and if it is, checks if the last
        # word in the sentence is also a key in self.nGramCounts,
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

        # creates empty candidates dictionary
        candidates = {}

        # checks the second to last and last words of the sentence.
        # if that bigram exists as a key in self.nGramCounts, then
        # updates dictionary candidates with that key's value, which
        # is a dictionary of possible third words and their counts
        if sentence[-2] in self.nGramCounts:
            if sentence[-1] in self.nGramCounts[sentence[-2]]:
                candidates.update(self.nGramCounts[sentence[-2]][sentence[-1]])

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

        # makes trigram_text a copy of text, then passes it through prepRhymingData
        trigram_text = copy.deepcopy(text)
        trigram_text = self.prepRhymingData(trigram_text)

        trigram_count = 1
        for i in range(len(trigram_text)):   # updates self.nGramCounts with trigram frequencies exactly
            j = len(trigram_text[i]) - 1     # like trainModel (see lines 45-60), except in reverse
            while j > 1:
                word1 = trigram_text[i][j]
                word2 = trigram_text[i][j - 1]
                word3 = trigram_text[i][j - 2]
                if word1 in self.nGramCounts:
                    if word2 in self.nGramCounts[word1]:
                        if word3 in self.nGramCounts[word1][word2]:
                            self.nGramCounts[word1][word2][word3] += 1
                        else:
                            self.nGramCounts[word1][word2].update({word3: trigram_count + 1})
                    else:
                        self.nGramCounts[word1].update({word2: {word3: trigram_count + 1}})
                else:
                    self.nGramCounts.update({word1: {word2: {word3: trigram_count}}})
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

        # checks if the sentence's second to last
        # word is a key in self.nGramCounts, and
        # if it is, checks if the last word in the
        # sentence is a key in keys2,
        # if so, then checks if self.nGramCounts
        # contains words that rhyme with that word
        # if so, returns true
        if sentence2 is None:   # if there is no rhyme-reference line
            keys1 = self.nGramCounts.keys()                  # makes keys1 a list of self.nGramCount's keys
            keys2 = self.nGramCounts[sentence1[-2]].keys()   # and keys2 a list of keys1's keys. then checks
            if sentence1[-2] in keys1:                       # that the last two words of sentence1 align with
                if sentence1[-1] in keys2:                   # keys1 and keys2, respectively
                    rhymable_keys = self.getCandidateDictionary(sentence1).keys()      # makes rhymable_keys a list
                    if len(rhymable_keys) != 0:                                        # of candidate words. returns
                        if (len(rhymable_keys) == 1) and ('$:::$' in rhymable_keys):   # false if that list only
                            return False                                               # contains '$:::$'
                        else:
                            for i in range(len(rhymable_keys)):                   # iterates through rhymable_keys and
                                if rhymable_keys[i] != '$:::$':                   # checks that it contains a word
                                    rhyming_list = rhyme_dict[rhymable_keys[i]]   # in keys1. this ensures that there
                                    for j in range(len(rhyming_list)):            # are other words in self.nGramCounts
                                        word = rhyming_list[j]                    # that rhyme with the word chosen
                                        if word in keys1:
                                            return True
        # checks the same conditions as
        # above except that it uses sentence1
        # as the rhyme-reference line
        else:
            keys1 = self.nGramCounts.keys()
            keys2 = self.nGramCounts[sentence2[-2]].keys()
            if sentence2[-2] in keys1:
                if sentence2[-1] in keys2:
                    rhymable_keys = self.nGramCounts[sentence2[-2]][sentence2[-1]].keys()
                    if len(rhymable_keys) != 0:
                        if (len(rhymable_keys) == 1) and ('$:::$' in rhymable_keys):
                            return False
                        else:
                            for i in range(len(rhymable_keys)):
                                if rhymable_keys[i] != '$:::$':
                                    rhyming_list = rhyme_dict[rhymable_keys[i]]
                                    compare_list = rhyme_dict[sentence1[-1]]
                                    for j in range(len(rhyming_list)):
                                        word = rhyming_list[j]
                                        if (word in keys1) and (word in compare_list):
                                            return True

        return False

    def trainingDataHasReverseNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 2
        Modifies: nothing
        Effects:  exactly the same as trainingDataHasNGram except
                  checks the reverse conditions in order to
                  correctly generate a sentence starting at the end
        """

        # checks if the sentence's second to first
        # word is a key in self.nGramCounts, and
        # if it is, checks if the first word in the
        # sentence is a key in self.nGramCounts[sentence[1]],
        # if so, returns true
        if sentence[1] in self.nGramCounts.keys():
            if sentence[0] in self.nGramCounts[sentence[1]].keys():
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
        Effects:  exact same as getCandidateDictionary except
                  that it uses the reverse conditions in order
                  to generate the sentence in reverse order
        """

        # creates empty candidates dictionary
        candidates = {}

        # checks the second word is a key in
        # self.nGramCounts. then checks if the first word
        # is a key in self.nGramCounts[1]. if so
        # then it updates dictionary candidates with that
        # key's value.
        if sentence[1] in self.nGramCounts:
            if sentence[0] in self.nGramCounts[sentence[1]]:
                candidates.update(self.nGramCounts[sentence[1]][sentence[0]])

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
        # rhymes with the last word in sentence.
        # if so, updates constrainedCandidates with
        # that key value pair
        for i in range(len(keys)):
            rhyming_list = rhyme_dict[keys[i]]
            for j in range(len(rhyming_list)):
                word = rhyming_list[j]
                if word in allCandidates:
                    update({word: allCandidates[keys[i]]})

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
    sentence = [ 'the', 'quick', 'brown' ]
    trigramModel = TrigramModel()
    print trigramModel.trainModel(text)
    print trigramModel.trainingDataHasNGram(sentence)
    print trigramModel.getCandidateDictionary(sentence)

