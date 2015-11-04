# -----------------------------------------------------------------------------
# The following 12 functions are stubbed for you. You must pass all of our
# test cases for these functions as part of the core. To run your functions
# with our test cases, run the file called runTests.py, which can be found in
# the warmup/ directory.

def returnDictionary(D):
    """
    Function 1.
    Returns the input dictionary D unchanged.
    """
    return

def keyInDict(D, K):
    """
    Function 2.
    Returns True if and only if the key K is already in the input dictionary D.
    """
    return

def returnKeyVal(D, K):
    """
    Function 3.
    Returns the value associated with the key K in the input dictionary D.
    """
    return

def setKeyVal(D, K, V):
    """
    Function 4.
    Sets the value associated with the key K in the input dictionary D to the
    the value V. Returns the dictionary D.
    """
    return

def setKeyValList(D, K, V1, V2, V3, V4):
    """
    Function 5.
    Sets the value associated with the input key K, which is a key in
    the input dictionary D, to be a list composed V1 through V4 in that order.
    Returns the dictionary D.
    """
    return

def asciiAssociate():
    """
    Function 6.
    Makes a new dictionary, called asciiDict, whose keys are the lowercase
    characters from a to z, and whose values are the associated ascii
    values from 97 to 122. Returns the dictionary asciiDict.
    """
    return

def getColor(favoriteColors, name):
    """
    Function 7.
    Returns the first element in the list associated with the key "name"
    in the input dictionary favoriteColors.
    """
    return

def translate(vocab, word, language):
    """
    Function 8.
    The input dictionary, vocab, could look something like this:
    { "hello": { "Spanish" : "hola", "French": "bonjour" } }
    Given the input dictionary, this function returns the value associated
    with the input word and language.
    """
    return

def nestedDictionary():
    """
    Function 9.
    Creates a new dictionary, D, where its keys are the lowercase characters
    from a to z, and each key has a value of an empty dictionary.
    Returns the new dictionary.
    """
    return

def nestedDictionary3D(L1, L2):
    """
    Function 10.
    Creates a 3D dictionary, D, with keys of each item of list L1.
    The value for each key in D is a dictionary, which
    has keys of each item of list L2 and corresponding values of empty
    dictionaries.
    Returns the new dictionary D.
    """
    return

def valueFrom3D(D, K1, K2, K3):
    """
    Function 11.
    Given the 3D input dictionary D, returns the value associated
    with the innermost dictionary accessed using keys K1, K2, and K3,
    in that order.
    """
    return

def keysIn2D(D, L1, L2):
    """
    Function 12.
    Given a 2D input dictionary D, returns True if and only if the last item of
    list L1 is a key in D, and that key is associated with a dictionary
    that contains the last item of list L2 as a key.
    """
    return



# -----------------------------------------------------------------------------
# Example tests for your own benefit. Write as many test cases as you need!

if __name__ == '__main__':
    D = { 'question' : 'answer' , 'hello': 'goodbye', 'hot' : 'cold' }

    # This should print True if Function 3 is implemented correctly
    print 'goodbye' == returnKeyVal(D, 'hello')


