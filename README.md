# Lyricist AI

### **Important Info**
  This originates from the completed version of the final project from EECS 183 at the University of Michigan, which I took in the fall   semester of 2016. Click [here](https://github.com/eecs183/creative-ai/wiki) for the original specifications. 

**Lyricist AI**
is an artificial intelligence that can generate song lyrics that sound
like they could be Colplay lyrics. They rhyme as well! <br><br>

### **rhymeLibrary.txt**
  My greatest challenge was getting a song's stanzas to have
  rhyming lines. I first tried using the external library,
  pronouncing.
  But, I found that pronouncing's phoneme library wasn't expansive enough,
  and didn't include slant rhymes.
  My next idea was to write a data scraper for Rhymezone.com. I was successful in this,
  but scraping Rhymezone for rhymes every time the AI needed to find rhyming words
  would take far too much time. I then noticed that Datamuse, Rhymezone's publisher,
  offers an API. Unfortunately, sending a request to Rhymezone through the API
  for every word still took too long. So, instead of sending a request for a word
  every time the program needs to find a rhyme, I decided to use pickle to create a .txt file containing
  a dictionary with key value pairs of every word in Coldplay's lyrics and a list
  of rhyming words. I call this file "rhymeLibrary.txt," and loading it into a local
  dictionary, whenever needed, takes under a second. The AI can then search through
  the local dictionary to find rhymes quickly and efficiently. <br><br>

### **How to Run**
1. My program runs best in *Command Prompt* or *Terminal*, please do not try
to run it in Git Bash.<br>

2. Click [here](https://github.com/hgorelick/Lyricist-AI/archive/master.zip) to download the repository. If the link doesn't work, please scroll to
the top of the page and click the green "clone or download" button.<br>

3. Once downloaded, unzip the folder. Next, open Command Prompt or Terminal
and navigate to the folder containing our repository.<br>

4. Now, enter "python generate.py" (without the quotes) into the command line.

5. Follow prompts and enjoy!

### **Future Goals**
I intend on editing the code so that the user can input an artist of their choice and receive the same results. I also will need to adapt/develop a grammar model in order to ensure that the lines not only rhyme, but make sense as well.

