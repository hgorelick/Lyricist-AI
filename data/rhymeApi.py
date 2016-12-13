#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
from nGramModel import *
from unigramModel import *
from bigramModel import *
from trigramModel import *
from datamuse import datamuse
import time


def api(word):
    """
    Requires: word is a string
    Modifies: nothing
    Effects:  uses datamuse api to return list
              of words that rhyme with word
    """

    # makes rhymer an instance of Datamuse class
    rhymer = datamuse.Datamuse()

    # makes rhymes_dict a list of dictionaries
    # that contain the rhyming words and some
    # extra info that we don't need
    perfect_rhymes = rhymer.words(rel_rhy=word)
    near_rhymes = rhymer.words(rel_nry=word)
    rhymes_dict = perfect_rhymes
    rhymes_dict += near_rhymes

    # removes unneeded key/value pairs from rhymes_dict
    exclude1 = 'score'
    exclude2 = 'numSyllables'
    for i in range(len(rhymes_dict)):
        for j in range(len(rhymes_dict[i])):
            if exclude1 in rhymes_dict[i]:
                del rhymes_dict[i][exclude1]
            elif exclude2 in rhymes_dict[i]:
                del rhymes_dict[i][exclude2]

    # makes u_rhymes a list of unicode strings
    # that rhyme with word
    u_rhymes = []
    for i in range(len(rhymes_dict)):
        u_rhymes += rhymes_dict[i].values()

    # converts unicode strings in u_rhymes to UTF8 strings
    # and assings this new list to rhymes
    rhymes = [i.encode('UTF8') for i in u_rhymes]

    #time.sleep(1)

    return rhymes


if __name__ == '__main__':
    print api('test')
