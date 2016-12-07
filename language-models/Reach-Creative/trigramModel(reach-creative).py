import random
from nGramModel import *
import copy
import pronouncing


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
        keys1 = self.nGramCounts.keys()
        keys2 = self.nGramCounts[sentence[-2]].keys()
        if sentence[-2] in keys1:
            if sentence[-1] in keys2:
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

    def trainingDataHasRhymingNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 2
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next rhyming token for the sentence.
        """

        # Checks if the sentence's second to last
        # word is a key in self.nGramCounts, and
        # if it is, checks if the last word in the
        # sentence is also a key in self.nGramCounts,
        # if so, then checks if self.nGramCounts
        # contains words that rhyme with that word
        # if so, returns true

        keys1 = self.nGramCounts.keys()
        keys2 = self.nGramCounts[sentence[-2]].keys()
        if sentence[-2] in keys1:
            if sentence[-1] in keys2:
                rhyming_list = pronouncing.rhymes(sentence[-1])
                for i in range(len(rhyming_list)):
                    word = rhyming_list[i]
                    word = str(word)
                    if word in keys2:
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
        rhyming_list = pronouncing.rhymes(sentence1[-1])
        for i in range(len(rhyming_list)):
            word = rhyming_list[i]
            if word in allCandidates:
                word = str(word)
                update({word: allCandidates[word]})

        return constrainedCandidates

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
        # rhymes with the last word in sentence1.
        # if so, updates constrainedCandidates with
        # that key value pair
        for i in range(len(keys)):
            rhyming_list = pronouncing.rhymes(keys[i])
            for j in range(len(rhyming_list)):
                word = rhyming_list[j]
                word = str(word)
                if word in self.getDictionary():
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

