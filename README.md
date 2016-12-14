# Coldplay Creative AI

**Coldplay Creative AI**
is an artificial intelligence that can generate song lyrics that sound
like they could be colplay lyrics. They rhyme as well! <br><br>

### **rhymeLibrary.txt**
  Our team's greatest challenge was getting a song's stanzas to have
  rhyming lines. We first tried using the external library,
  pronouncing.
  But, we found that pronouncing's phoneme library wasn't expansive enough,
  and didn't include slant rhymes.
  Our next idea was to write a data scraper for Rhymezone.com. We were successful in this,
  but scraping Rhymezone for rhymes every time we needed to find rhyming words
  would take far too much time. We then realized that Datamuse, Rhymezone's publisher,
  offers an API. Unfortunately, sending a request to Rhymezone through the API
  for every word still took too long. So, instead of sending a request for a word
  every time we needed to find a rhyme, we decided to use pickle create a txt file containing
  a dictionary with key value pairs of every word in Coldplay's lyrics and a list
  of rhyming words. We call this file rhymeLibrary, and loading it into a local
  dictionary, whenever needed, takes under a second. We can then search through
  the local dictionary to find rhymes quickly and efficiently. <br><br>

### **How to Run**
1. Our program runs best in *Command Prompt* or *Terminal*, please do not try
to run it in Git Bash.<br>

2. Click [here](https://github.com/eecs183/Creative_AI_31_Repository.git) to download our repository. If the link doesn't work, please scroll to
the top of the page and click the green "clone or download" button.<br>

3. Once downloaded, unzip the folder. Next, open Command Prompt or Terminal
and navigate to the folder containing our repository.<br>

4. Now, enter "python generate.py" (without the quotes) into the command line.

5. Follow prompts and enjoy!

