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
        dirs = [normalize('NFC', unicode(item, 'utf-8')) for \
            item in os.listdir(musicDir)]
        dirName = unicode(dirName, 'utf-8')

        if normalize('NFC', dirName) not in dirs:
        # check if this artist has a directory in the lyrics directory
            print "No artist named", dirName, "in directory", musicDir
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


    def loadMusic(self, platform):
        """
        Loads the midi files to the specified platform directory by
        extracting data out of those midi .txt files and converting that
        data into PySynth tuple format, then adding each song's list of
        tuples to the self.songs list.
        """
        midiDir = os.path.dirname(os.path.abspath(__file__)) + "/midi/"
        platformDir = midiDir + platform

        if platform not in os.listdir(midiDir):
            print "No platform named", platform, "in directory", midiDir
            return

        midiFiles = os.listdir(platformDir)
        midiFiles = [platformDir + "/" + midiFile for midiFile in midiFiles]

        for midiFile in midiFiles:
            F = open(midiFile, "r")
            lines = F.readlines()
            F.close()

            song = []
            for line in lines:
                line = line.split()

                # extract pitch and duration from .txt song data, convert
                # those values to pysynth format, and add the
                # (pitch, duration) tuple to the song list
                if "TR" in line and line[line.index("TR") + 1] == "1" \
                        and "NT" in line:
                    noteIndex = line.index("NT")
                    pitch = line[noteIndex + 1]
                    pitch = self.formatPitch(pitch)

                    duration = line[noteIndex + 2]
                    duration = self.formatDuration(duration)

                    pysynthTuple = (pitch, duration)
                    song.append(pysynthTuple)

            if song:
                self.songs.append(song)


    def formatPitch(self, asciiPitch):
        """
        Converts from the ASCII representation of a note's pitch to the
        PySynth representation of a note's pitch, returning the
        converted string.
        """
        pitch = asciiPitch.lower()

        # get octave value relative to 4
        octave = 4
        if "'" in pitch:
            numApostrophes = pitch.count("'")
            octave += numApostrophes
            if octave >= 8:
                octave = 7
            pitch = pitch.replace("'", "")
        elif "-" in pitch:
            numDashes = pitch.count("-")
            octave -= numDashes
            if octave <= 0:
                octave = 1
            pitch = pitch.replace("-", "")

        # i don't think pysynth likes e# or b#
        if pitch == "e#":
            pitch = "f"
        elif pitch == "b#":
            pitch = "c"

        # these shouldn't be a problem - test these
        if pitch.count("#") > 1:
            pitch = pitch[0] + "#"
        elif pitch.count("b") > 2:
            pitch = pitch[0] + "b"

        pitch += str(octave)
        return pitch

    def formatDuration(self, asciiDuration):
        """
        Converts from the ASCII representation of a note's duration to the
        PySynth representation of a note's duration, as described in
        the spec. Returns the integer representing the duration.
        """
        duration = re.split("[+ /]", asciiDuration)

        if len(duration) == 1:
            duration = float(duration[0])
        elif len(duration) == 2:
            nominator = float(duration[0])
            denominator = float(duration[1])
            try:
                duration = nominator / denominator
            except ZeroDivisionError:
                duration = nominator
        elif len(duration) == 3:
            wholeNumber = float(duration[0])
            nominator = float(duration[1])
            denominator = float(duration[2])
            try:
                duration = wholeNumber + nominator / denominator
            except ZeroDivisionError:
                duration = wholeNumber
        else: # should never get here
            duration = 1

        if duration < 0.5:
            duration = 16
        elif duration >= 0.5 and duration < .75:
            duration = -8
        elif duration >= 0.75 and duration < 1:
            duration = 8
        elif duration >= 1 and duration < 1.5:
            duration = 4
        elif duration >= 1.5 and duration < 2:
            duration = -4
        elif duration >= 2 and duration < 3:
            duration = 2
        elif duration >= 3 and duration < 4:
            duration = -2
        else:
            duration = 1

        return duration

if __name__ == "__main__":
    dataLoader = DataLoader()
    dataLoader.loadLyrics('the_beatles')
    # put any testing code needed here

