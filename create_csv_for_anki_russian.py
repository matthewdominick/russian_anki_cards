import csv
import requests
from bs4 import BeautifulSoup
import re

#input_filename = 'Lesson2_Page4_nouns.csv'
#input_filename = 'adjectives.csv'
input_filename = 'inputs/verb_infinitives.csv'


output_filename = 'output.csv' #note, this file gets deleted first if present.  
audio_folder = '/audio/'

#--------------------------------------------------------------------------------

# Returns list of Russian Words from the input CSV file
def extractRussianWordsFromCSV(filename):
    russian_words=[]
    with open(input_filename, newline='') as csvfile:
        word_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in word_reader:
            russian_words.extend(row)
    return russian_words
#--------------------------------------------------------------------------------



#--------------------------------------------------------------------------------
''' 
Returns Beautiful Soup Page Text File
Input is list of russian words in the following forms
  Verbs - Russian Imperfective Infinitive
  Nouns - Nominative singular
  Adjective - Nominative masculine singular
Requires the requests module/library
'''
def getBSPageTextObject(russian_word):
    url = 'https://en.openrussian.org/ru/' + str(russian_word)
    page = requests.get(url)
    if page.status_code==200: #This is not working. The error page is a 200.  
        soup = BeautifulSoup(page.text, 'html.parser')
    else:
        soup = 'fail'
    return soup
#--------------------------------------------------------------------------------



#--------------------------------------------------------------------------------
def getEnglishTranslation(soupText):
    if soupText!='fail':
        englishTranslation = soupText.find_all(class_=['editable'])[0].getText()
        englishTranslation=englishTranslation.strip('\n').strip('1.').strip()
        englishTranslation = englishTranslation.replace(",", " -")
        return englishTranslation
    else:
        return 'Translation not found'
#--------------------------------------------------------------------------------


#--------------------------------------------------------------------------------
def getAudioURL(russian_word):
    #audioURL = soupText.find('audio').get('src') #this line does not work on all cases
    audioURl = 'https://en.openrussian.org/read/ru/'+russian_word
    return audioURL
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------

def checkIfRussianWordExists(soupText):
    """
    Check if word exists on openrussian.org
    """	
    audioURL = soupText.find('audio').get('src')
    x=1
    x=0
    if x==1:	
        return True
    else:
        return False
#--------------------------------------------------------------------------------


russian_words = extractRussianWordsFromCSV(input_filename)

target = open(output_filename, 'w')
target.truncate() #delete contents of file if it exists

i=0
for words in russian_words:
    soupText = getBSPageTextObject(russian_words[i])
    englishTranslation = getEnglishTranslation(soupText)
    #audioURL = getAudioURL(soupText)
    #print (russian_words[i]+","+englishTranslation+","+audioURL)
    print (russian_words[i]+","+englishTranslation)
    target.write(russian_words[i]+","+englishTranslation)
    target.write(",[sound:"+russian_words[i]+".mp3]")
    target.write("\n")
    audioURl = 'https://en.openrussian.org/read/ru/'+russian_words[i]
    r = requests.get(audioURl)
    print (r.status_code)
    if r.status_code==200:
        with open(russian_words[i]+'.mp3', 'wb') as f:  
            f.write(r.content)
    else:
        print ('Could not find audio for '+russian_words[i])
    i=i+1
target.close()

