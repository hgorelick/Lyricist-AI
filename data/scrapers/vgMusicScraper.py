from baseScraper import *


class VGMusicScraper(BaseScraper):

    def __init__(self):
        """
        This is the constructor for the VGMusic scraper.
        It sets the data needed for the scraper.
        """
        self.hostUrl = "www.vgmusic.com"
        self.platformsFile = "vgMusicPlatforms.txt"
        self.platforms = {}
        self.fullPlatform = ""
        self.delay = 1.0

    def getUserPlatform(self):
        """
        This function loads the platforms from the vgMusicPlatforms.txt
        file, then asks the user to input a platform to download
        MIDI files from, and keeps asking until the user inputs a
        valid platform in the self.platforms dictionary.
        """
        F = open(self.platformsFile, "r")
        lines = F.readlines()
        F.close()

        for line in lines:
            line = line.split("\t")
            self.platforms[line[1]] = [line[0], line[2].strip()]

        confirmation = "n"
        userPlatform = ""

        while confirmation != "y":
            prompt = "Download music for which platform (no spaces)? "
            userPlatform = raw_input(prompt)
            userPlatform = userPlatform.lower()
            if userPlatform in self.platforms:
                print "Do you mean the", self.platforms[userPlatform][0],
                print userPlatform + "?"
                confirmation = raw_input("Please confirm (y/n): ")
            else:
                print "Platform", userPlatform, "is not available at",
                print self.hostUrl + "."
                print "Please check vgMusicPlatforms.txt for the full list."

        self.fullPlatform = self.platforms[userPlatform][0] + " " + userPlatform
        return userPlatform, self.platforms[userPlatform][1]

    def scrape(self, platform, path):
        """
        This function scrapes the relevant platform music from the vgmusic
        site and saves the MIDI files to the data/midi/<platform> directory.
        """
        midiDir = "../midi/" + platform

        if not os.path.exists(midiDir):
            subprocess.call("mkdir " + midiDir, shell=True)

        html = self.getPageHtml(path)
        midiPattern = re.compile('"(.*?.mid)"')
        midiMatches = re.findall(midiPattern, html)

        if len(os.listdir(midiDir)) == len(midiMatches):
            return

        print "Found", len(midiMatches), "midi files for", self.fullPlatform
        progress = 0
        for match in midiMatches:
            progress = self.updateProgressBar(progress, match, len(midiMatches))
            url = "http://" + self.hostUrl + "/" + path + "/" + match
            try:
                response = urllib2.urlopen(url)
                midiFile = midiDir + "/" + match
                destination = open(midiFile, "w+")
                destination.write(response.read())
            except urllib2.HTTPError:
                pass

        print "\nScraped data for", self.fullPlatform, "successfully\n"

    def convertMidiToAscii(self, midiDir):
        """
        Takes the midi files in the midiDir directory and runs the mid2asc C
        executable to convert them into .txt files, then deletes the midi
        files. Also deletes any files that failed to convert properly.

        This function could potentially be used to convert MIDI files to
        ASCII files for music other than the music from the VGmusic site
        (i.e. if one wanted to manually or automatically download music
        from different sites).
        """
        print "Converting midi files to .txt files"
        midiFiles = os.listdir(midiDir)

        update = 0
        for midiFile in midiFiles:
            update = self.updateProgressBar(update, midiFile, len(midiFiles))
            if midiFile[-4:] == ".mid":
                midiFile = midiDir + "/" + midiFile
                midiTextFile = midiFile[:-4] + ".txt"

                convertCommand = "../midi/mid2asc " + midiFile + \
                                 " > " + midiTextFile
                FNULL = open(os.devnull, "w")
                returnCode = subprocess.call(convertCommand, stdout=FNULL, \
                                             stderr=subprocess.STDOUT, \
                                             shell=True)
                removeCommand = "rm " + midiFile
                subprocess.call(removeCommand, shell=True)

                if returnCode != 0:
                    removeCommand = "rm " + midiTextFile
                    subprocess.call(removeCommand, shell=True)

        print "\nConverted all midi files in", self.fullPlatform,
        print "directory to .txt files"


if __name__ == "__main__":
    scraper = VGMusicScraper()
    platform, path = scraper.getUserPlatform()
    scraper.scrape(platform, path)
    scraper.convertMidiToAscii("../midi/" + platform)

