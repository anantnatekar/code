import nltk
import os
import re
import numpy as np  
import random  
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path

#the below sentence to be run once only. After its downloaded the sentence can be commented
#nltk.download('stopwords')

ps = PorterStemmer() #invoking method for stemming
feature_id = 0 #defining constants
wordfreq = {} #defining constants
path = '/Users/nat2147/anant/school/marquette/data mining/mini_newsgroups/'
for root, directories, files in os.walk(path):
    for name in files:
        #if name in ('75895','76277','76284','76080','76410','76073','76020'):
        if not os.path.exists(name):
            print('file does not exist', name) #test
        else:
            f = open(name, 'r', errors='ignore')
            content = f.readlines() #reads all the lines of a file
            for sentence in content:
                tokens = nltk.word_tokenize(sentence) #tokenizes the sentence
                for token in tokens:
                    token = token.lower() #lower case
                    token = ps.stem(token) #stemming
                    #print(token) #for debugging
                    token = re.sub(r'\W',' ',token) #removes punctuation
                    token = re.sub(r'\s+',' ',token) #removes empty text
                    stop_word = set(stopwords.words('english')) 
                    if token not in stop_word: #removes stop words
                        if token not in wordfreq.keys(): #counts number of words
                            wordfreq[token] = 1
                            feature_id += 1 #Append feature id to the wordfreq 
                            wordfreq = {token:feature_id}
                        else:
                            wordfreq[token] += 1
                            feature_id += 1 #Append feature id to the wordfreq 
                            wordfreq = {token:feature_id}
            f.close()

with open('training_dataset.txt', 'w') as f:
    print(wordfreq, file=f)
#print(wordfreq)


'''
####
Code for making the bag of words into boolean model
####
sentence_vectors = []
for sentence in content:
    sentence_tokens = nltk.word_tokenize(sentence)
    sent_vec = []
    for token in wordfreq:
        if token in sentence_tokens:
            sent_vec.append(1)
        else:
            sent_vec.append(0)
    sentence_vectors.append(sent_vec)

#print(wordfreq)
'''