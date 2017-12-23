import csv
import requests
from bs4 import BeautifulSoup
import re

input_filename = 'Lesson2_Page3_nouns.csv'
output_filename = 'output.csv' #note, this file gets deleted first if present.  

#--------------------------------------------------------------------------------

# Returns list of Russian Words from the input CSV file
def extractRussianWordsFromCSV(filename):
    russian_words=[]
    with open(input_filename, newline='') as csvfile:
        word_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in word_reader:
            #print(''.join(row))
            russian_words.extend(row)
            #print(len(row))
            #print(row)
    return russian_words
#--------------------------------------------------------------------------------



#--------------------------------------------------------------------------------
''' 
Returns BS Page Text File
Input is list of russian words in the following forms
  Verbs - Russian Imperfective Infinitive
  Nouns - Nominative singular
  Adjective - Nominative masculine singular
Requires the requests module/library
'''
def getBSPageTextObject(russian_words):
    url = 'https://en.openrussian.org/ru/' + str(russian_words[i])
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup
#--------------------------------------------------------------------------------



#--------------------------------------------------------------------------------
def getEnglishTranslation(soupText):
    englishTranslation = soupText.find_all(class_=['editable'])[0].getText()
    englishTranslation=englishTranslation.strip('\n').strip('1.').strip()
    englishTranslation = englishTranslation.replace(",", " -")
    return englishTranslation
#--------------------------------------------------------------------------------


#--------------------------------------------------------------------------------
def getAudioURL(soupText):
    audioURL = soupText.find('audio').get('src')
    return audioURL
#--------------------------------------------------------------------------------




russian_words = extractRussianWordsFromCSV(input_filename)

target = open(output_filename, 'w')
target.truncate() #delete contents of file if it exists

i=0
for words in russian_words:
    soupText = getBSPageTextObject(russian_words)
    englishTranslation = getEnglishTranslation(soupText)
    audioURL = getAudioURL(soupText)
    print (russian_words[i]+","+englishTranslation+","+audioURL)
    target.write(russian_words[i]+","+englishTranslation+","+audioURL)
    target.write("\n")
    i=i+1
target.close()

