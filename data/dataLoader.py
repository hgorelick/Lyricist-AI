#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from unicodedata import normalize


class DataLoader(object):

    def __init__(self):
        """
        This is the DataLoader constructor, which sets up data for the
        lyrics portion of the project and the music portion of the
        project.

        The lyrics portion sets up a blank list, self.lyrics,
        for the lyrics to be loaded into, which will become a list
        of lists of words to be used in NGramModels. It also
        instantiates regular expression member variables for
        patterns to be found in the raw data.

        The music portion sets up a blank list, self.songs, which
        will become a list of lists of PySynth tuples to be
        used in generateMusic.py. Each inner list in self.songs
        is a list of all the notes of exactly one midi file.
        """
        # Lyrics
        self.lyrics = []
        self.spaceRegex = re.compile("\s+")
        self.punctuationRegex = re.compile("[,.;:!\*?\\/()'\"\-_]")
        self.bracketRegex = re.compile("\[.*?\]")

        # Music
        self.songs = []

    def loadLyrics(self, dirName):
        """
        Loads the lyrics files from the directory specified by dirName,
        if that directory exists. For each line in each file,
        cleans that line by removing punctuation and extraneous
        whitespaces, and lowercasing all words in the line. Finally, adds
        the line to the self.lyrics list, where a line is a list of words.
        """
        scriptDir = os.path.dirname(os.path.abspath(__file__))
        musicDir = os.path.join(scriptDir, "lyrics/")
        dirs = [normalize('NFC', str(item, 'utf-8')) for \
            item in os.listdir(musicDir)]
        dirName = str(dirName, 'utf-8')

        if normalize('NFC', dirName) not in dirs:
        # check if this artist has a directory in the lyrics directory
            print("No artist named", dirName, "in directory", musicDir)
            return

        artistDir = musicDir + dirName + "/"
        songs = os.listdir(artistDir)
        for song in songs:
            songFile = open(artistDir + song)
            songLines = songFile.readlines()
            songFile.close()

            # clean each line in each song and add it to self.lyrics
            for line in songLines:
                line = re.sub(self.bracketRegex, "", line)
                line = re.sub(self.punctuationRegex, "", line)
                line = re.sub(self.spaceRegex, " ", line)
                line = line.lower()
                line = line.strip().split()
                line = [word for word in line if word != ""]
                if line:
                    self.lyrics.append(line)

if __name__ == "__main__":
    dataLoader = DataLoader()
    dataLoader.loadLyrics('the_beatles')
    # put any testing code needed here

