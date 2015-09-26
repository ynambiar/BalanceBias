from bs4 import BeautifulSoup
import re

#global variables
files = ["wsjTest", "nytTest", "msnTest", "cnnTest"]

#methods
def getTitle(soup):
    return soup.html.head.title.string

def getHTML(filename):
    return filename + ".html"

#translates html to paragraphs/text
def writeToFile(filename, paragraphs, soup):
    file = open(filename, "w")
    for each in paragraphs:
        para = each.string
        if para is not None:
            file.write(para.encode("utf-8"))
    file.close()

#tokenizes text into sentences
def tokenizer_SENT(txt):
    return (re.findall(r'(?ms)\s*(.*?(?:\.|\?|!))', txt))  # split sentences

#returns array of sentence strings
def makeSentenceArray(filename):
    parsed = open(filename)
    sentences = tokenizer_SENT(parsed.read())
    return sentences

#reads html into file
def generateTxt():
    for each in files:
        soup = BeautifulSoup(open(getHTML(each)))
        paragraphs = soup("p")
        writeToFile(each + "_parsed.txt", paragraphs, soup)


#main()
print makeSentenceArray("wsjTest_parsed.txt")


























