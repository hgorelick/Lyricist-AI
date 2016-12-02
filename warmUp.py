# -----------------------------------------------------------------------------
# The following 12 functions are stubbed for you. You must pass all of our
# test cases for these functions as part of the core. To run your functions
# with our test cases, run the file called runTests.py, which can be found in
# the warmup/ directory.

def returnDictionary(D):
    """
    Requires: Nothing
    Modifies: Nothing
    Effects:  Returns the input dictionary D unchanged.
    """
    return D

def keyInDict(D, K):
    """
    Requires: D is a dictionary
    Modifies: Nothing
    Effects:  Returns True if and only if the key K is already in D.
    """
    if K in D:
        return True
    return False

def returnKeyVal(D, K):
    """
    Requires: D is a dictionary and K is a key in D
    Modifies: Nothing
    Effects:  Returns the value associated with K in the dictionary D.
    """
    return D[K]

def setKeyVal(D, K, V):
    """
    Requires: D is a dictionary
    Modifies: D
    Effects:  Sets the value associated with the key K in the dictionary D
              to be the value V. Returns the dictionary D.
    """
    D[K] = V
    return D

def setKeyValList(D, K, V1, V2, V3, V4):
    """
    Requires: D is a dictionary
    Modifies: D
    Effects:  Sets the value associated with the key K, which is a key in
              the input dictionary D, to be a list composed of V1 through
              V4, in that order. Returns the dictionary D.
    """
    val_list = [V1, V2, V3, V4]
    D[K] = val_list
    return D

def asciiAssociate():
    """
    Requires: Nothing
    Modifies: Nothing
    Effects:  Makes a new dictionary, called asciiDict, whose keys are
              the lowercase characters from a to z, and whose values are
              the associated ascii values from 97 to 122. Returns the
              dictionary asciiDict.
    """
    asciiDict = {}
    letter = 'a'
    value = 97
    i = 0

    while value <= 122:
        asciiDict.update({letter : value})
        i += 1
        letter = (chr(ord(letter) + 1))
        value += 1

    return asciiDict

def getColor(favoriteColors, name):
    """
    Requires: favoriteColors is a dictionary and name is a key in
              favoriteColors
    Modifies: Nothing
    Effects:  Returns the first element in the list associated with the
              key "name" in the input dictionary favoriteColors.
    """
    if name in favoriteColors:
        return favoriteColors[name][0]

def translate(vocab, word, language):
    """
    Requires: vocab is a 2-dimensional dictionary, word is a key in vocab,
              and language is a key in the dictionary that word maps to
    Modifies: Nothing
    Effects:  The input dictionary, vocab, could look something like this:
              { "hello": { "Spanish" : "hola", "French": "bonjour" } }
              Given the input dictionary, this function returns the
              value associated with the input word and language.
    """
    return vocab[word][language]

def nestedDictionary():
    """
    Requires: Nothing
    Modifies: Nothing
    Effects:  Creates a new dictionary, D, where its keys are the
              lowercase characters from a to z, and each key has a value
              of an empty dictionary. Returns the new dictionary D.
    """
    D = {}
    letter = 'a'
    i = 0

    while letter <= 'z':
        D.update({letter : {}})
        letter = (chr(ord(letter) + 1))
        i += 1

    return D

def nestedDictionary3D(L1, L2):
    """
    Requires: L1 and L2 are lists
    Modifies: Nothing
    Effects:  Creates a 3D dictionary, D, with keys of each item of list L1.
              The value for each key in D is a dictionary, which
              has keys of each item of list L2 and corresponding
              values of empty dictionaries. Returns the new dictionary D.
    """
    D = {}
    j = 0
    for i in range(len(L1)):
        while j <= range(len(L1)):
            k = 0
            while k <= range(len(L2)):
                D.update({L1[j] : {L2[j] : {}}})
                k += 1
            j += 1
    return D

def valueFrom3D(D, K1, K2, K3):
    """
    Requires: D is a 3D dictionary, K1 is a key in D, K2 is a key in the
              dictionary that K1 maps to, and K3 is a key in the dictionary
              that K2 maps to
    Modifies: Nothing
    Effects:  Given the 3D input dictionary D, returns the value associated
              with the innermost dictionary accessed using keys K1, K2, and K3,
              in that order.
    """
    return D[K1][K2][K3]

def keysIn2D(D, L1, L2):
    """
    Requires: D is a 2D dictionary, L1 is a list, and L2 is a list
    Modifies: Nothing
    Effects:  Given a 2D input dictionary D, returns True if and only
              if the last item of list L1 is a key in D, and that key
              is associated with a dictionary that contains the last
              item of list L2 as a key.
    """
    L1_checker = L1[-1]
    L2_checker = L2[-1]

    if (L1_checker in D) and (L1_checker in L2) and (L2_checker in D):
        return True
    return False

def newCopy(L1):
    """Function 13.
    Given a List L1, return a tuple of (L1, L2) where L2 is an exact copy of L1
    but with this appended value: 183
    """

    L2 = L1[:]
    L2.append(183)

    return L1, L2


# -----------------------------------------------------------------------------
# Example tests for your own benefit. Write as many test cases as you need!

if __name__ == '__main__':
    D = { 'question' : 'answer' , 'hello': 'goodbye', 'hot' : 'cold' }

    # This should print True if Function 3 is implemented correctly
    print 'goodbye' == returnKeyVal(D, 'hello')


