
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

def readFile(filePath):

  s = ''

  #File is opened in read mode

  with open(filePath,'r') as f:

    #Loop gather content from doc

    for i in f:

      #Convert to lower case

      s += ' '.join(i.split()).lower()

  return s

#Main Code
#Create object for posterStemmer

PorterS = PorterStemmer()

#Stop words
stop_words = set(stopwords.words('english'))

#call mwethod to Read file you should give your path as parameter instead of '/content/drive/My Drive/Colab Notebooks/result1.txt'
document = readFile('.txt')

#Token converter
word_tokens = word_token(document)

#Stem content
filter_sentence = [ps.stem(w) for w in word_tokens if not w in stop_words]  

print("File content before stem:\n",word_tokens)

print("\nFile content after stem:\n",filter_sentence)

#Andrew's code ends here

#
#dictionary = {'Hi', 'Hello', 'Good', 'morning'}
#counter = 0
#for term in dictionary:
#    dict1 = dict.fromkeys(term, counter)
#    counter = counter + 1
    
#f = open("feature_definition_file.txt","w")
#f.write( str(dict1) )
#f.close()
#
details={'Name' : "Alice", 
		'Age' : 21, 
		'Degree' : "Bachelor Cse", 
		'University' : "Northeastern Univ"} 

with open("myfile.txt", 'w') as f: 
	for key, value in details.items(): 
		f.write('%s:%s\n' % (key, value))


