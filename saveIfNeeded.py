"""
elif sentenceTooLong(desiredLength, len(sentence)):   # if the line reaches desiredLength, performs the
                                                               # checkRhymableSentence sequence (line 138), except
                                                               # here, next_word isn't '$:::$'
                    if not checkForRhyme(sentence1, sentence):
                        return sentence
                    else:
                        remove(next_word)
                        i -= 1
                        continue
                else:
                    return sentence
            else:   # if the line isn't rhymable, chooses a different word
                remove(sentence[-1])
                compare = selected_model.getNextToken(sentence)
                if compare == next_word:    # if that word is the same as it was before, removes the penultimate
                    remove(sentence[-1])    # word as well and returns to the top
                    continue
"""