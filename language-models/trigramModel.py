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

        # Makes a copy of text, then passes it through prepData
        trigram_text = copy.deepcopy(text)
        #reversed_trigram = [sublist[::-1] for sublist in trigram_text]
        trigram_text = self.prepRhymingData(trigram_text)

        # Counts frequency of each trigram in text_copy
        # then updates the self.nGramCounts dictionary
        # as specified by the spec
        trigram_count = 1
        for i in range(len(trigram_text)):
            j = len(trigram_text[i]) - 1
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
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next rhyming token for the sentence.
        """
        rhyme_library = open(
            r'/data/rhymeLibrary.txt',
            'rb')
        rhyme_dict = pickle.load(rhyme_library)

        # checks if the sentence's second to last
        # word is a key in self.nGramCounts, and
        # if it is, checks if the last word in the
        # sentence is a key in keys2,
        # if so, then checks if self.nGramCounts
        # contains words that rhyme with that word
        # if so, returns true
        if sentence2 is None:
            keys1 = self.nGramCounts.keys()
            keys2 = self.nGramCounts[sentence1[-2]].keys()
            if sentence1[-2] in keys1:
                if sentence1[-1] in keys2:
                    rhymable_keys = self.nGramCounts[sentence1[-2]][sentence1[-1]].keys()
                    if len(rhymable_keys) != 0:
                        if (len(rhymable_keys) == 1) and ('$:::$' in rhymable_keys):
                            return False
                        else:
                            for i in range(len(rhymable_keys)):
                                if rhymable_keys[i] != '$:::$':
                                    rhyming_list = rhyme_dict[rhymable_keys[i]]
                                    for j in range(len(rhyming_list)):
                                        word = rhyming_list[j]
                                        if word in keys1:
                                            return True
        # checks the same conditions as above,
        # and then checks if the words in rhyming_list
        # rhyme with the last word of sentence.
        # if so, returns true
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

        # Checks if the sentence's last
        # word is a key in self.nGramCounts, and
        # if it is, checks if the second to last word in the
        # sentence is a key in self.nGramCounts[sentence[-1]],
        # if so, returns true
        if sentence[-1] in self.nGramCounts.keys():
            if sentence[-2] in self.nGramCounts[sentence[-1]].keys():
                return True
        return False

    def getRhymingCandidateDictionary(self, sentence1, sentence2):
        """
        Requires: same as getCandidateDictionary
        Modifies: nothing
        Effects:  same as getCandidateDictionary except the
                  the candidate words will rhyme with the last word
                  of the compared sentence.
        """
        rhyme_library = open(
            r'/data/rhymeLibrary.txt',
            'rb')
        rhyme_dict = pickle.load(rhyme_library)

        # Makes allCandidates the returned dictionary of getCandidateDictionary
        allCandidates = self.getCandidateDictionary(sentence2)

        # Filters out symbol, it can't rhyme so
        # shouldn't be returned
        exclude = '$:::$'
        if exclude in allCandidates:
            del allCandidates[exclude]

        # Makes constrainedCandidates an empty dictionary
        constrainedCandidates = {}

        # Helps optimize for loop
        update = constrainedCandidates.update

        # Checks if any of the words in allCandidates
        # rhymes with the last word in sentence1.
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
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  only used for the last word of
                  sentence in generateSentence. ensures
                  that it will be possible for the rest
                  of the sentences in the verse or the
                  chorus can rhyme
        """
        rhyme_library = open('rhymeLibrary.txt', 'rb')
        rhyme_dict = pickle.load(rhyme_library)

        # Makes allCandidates the returned dictionary of getCandidateDictionary
        allCandidates = self.getCandidateDictionary(sentence)

        # Filters out symbol, it can't rhyme so
        # shouldn't be returned
        exclude = '$:::$'
        if exclude in allCandidates:
            del allCandidates[exclude]

        keys = allCandidates.keys()

        # Makes constrainedCandidates an empty dictionary
        constrainedCandidates = {}

        # Helps optimize for loop
        update = constrainedCandidates.update

        # Checks if any of the words in allCandidates
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

