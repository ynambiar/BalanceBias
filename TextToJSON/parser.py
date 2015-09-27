from bs4 import BeautifulSoup
import re

##methods

#return title of article
def getTitle(soup):
    return soup.html.head.title.string

#return html filename
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

#reads html into file
def generateTxt():
    for each in files:
        soup = BeautifulSoup(open(getHTML(each)))
        paragraphs = soup("p")
        writeToFile(each + "_parsed.txt", paragraphs, soup)

#tokenizes text into sentences
def tokenizer_SENT(txt):
    return (re.findall(r'(?ms)\s*(.*?(?:\.|\?|!))', txt))  # split sentences

#returns array of sentence strings
def makeSentenceArray(filename):
    parsed = open(filename + "_parsed.txt")
    sentences = tokenizer_SENT(parsed.read())
    return sentences

#converts array of string to json format
def writeToCSVjson(filename):
    count = 0
    sentences = makeSentenceArray(filename)

    file = open(filename + "_parsed.json", "w")
    file.write("{\"Inputs\":\n[\n")
    for each in sentences:
        output_format = '    {{"Id": "{id}", "Text": "{text}"}},\n'
        file.write(output_format.format( id = count,
                                        text = each))
        count = count + 1

    file.write("]}")
    file.close()

#generates .json files from source files (.html)
def generateJSONFromSource(source):
    for each in source:
        writeToCSVjson(each)

#main
source_files = ["wsjTest", "nytTest", "msnTest", "cnnTest"]
generateJSONFromSource(source_files)



