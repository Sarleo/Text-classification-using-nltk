# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 11:49:41 2018

@author: saranshmohanty
"""

import nltk
from nltk.stem.lancaster import LancasterStemmer

# stemmer
stemmer=LancasterStemmer()
training_data=[]

training_data.append({"class":"greeting", "sentence":"how are you?"})
training_data.append({"class":"greeting", "sentence":"how is your day?"})
training_data.append({"class":"greeting", "sentence":"good day"})
training_data.append({"class":"greeting", "sentence":"how is it going today?"})

training_data.append({"class":"goodbye", "sentence":"have a nice day"})
training_data.append({"class":"goodbye", "sentence":"see you later"})
training_data.append({"class":"goodbye", "sentence":"have a nice day"})
training_data.append({"class":"goodbye", "sentence":"talk to you soon"})
training_data.append({"class":"goodbye", "sentence":"bye"})
training_data.append({"class":"sandwich", "sentence":"make me a sandwich"})
training_data.append({"class":"sandwich", "sentence":"can you make a sandwich?"})
training_data.append({"class":"sandwich", "sentence":"having a sandwich today?"})
training_data.append({"class":"sandwich", "sentence":"what's for lunch?"})

print( "%s sentences of training data" %len(training_data))

# capture stemmed words in corpus
corpus_words={}
class_words={}

# turn a list into a set of unique items and then to a list again to remove duplicate items

classes=list(set(a['class'] for a in training_data))
for c in classes:
    #prepare a list of words within each class
    class_words[c]=[]
    
#loop through training_data
for data in training_data:
    #tokenise
    for word in nltk.word_tokenize(data['sentence']):
        #ignore some things
        if word not in ["?","'s"]:
            #stem and lowercase every friggin word
            stemmed_word=stemmer.stem(word.lower())
            #frequency analysis
            if stemmed_word not in corpus_words:
                corpus_words[stemmed_word]=1
            else:
                corpus_words[stemmed_word]+=1
                
            #add to class list, stems the training data
            class_words[data['class']].extend([stemmed_word])
            
# the frequency of every stemmed word is noted for every 
print("Corpus words and counts: %s \n"%corpus_words)
print("Class words: %s" %class_words)

##########################################equal weight##################################
#scoring
def calculate_class_score(sentence,class_name,show_details=True):
    score=0
    # tokenize sentence
    for word in nltk.word_tokenize(sentence):
        # check if the word belongs to any class or not
        if stemmer.stem(word.lower()) in class_words[class_name]:
            #same weight
            score+=1
            if show_details:
                print(" match: %s" %stemmer.stem(word.lower() ))
                
    return score
sentence = "bad day ?"

# now we can find the class with the highest score
for c in class_words.keys():
    print ("Class: %s  Score: %s \n" % (c, calculate_class_score(sentence, c)))

#####################################weighted#########################################
    # calculate a score for a given class taking into account word commonality
def calculate_class_score_wt(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with relative weight
            score += (1 / corpus_words[stemmer.stem(word.lower())])

            if show_details:
                print ("   match: %s (%s)" % (stemmer.stem(word.lower()), 1 / corpus_words[stemmer.stem(word.lower())]))
    return score



for c in class_words.keys():
    print ("Class: %s  Score: %s \n" % (c, calculate_class_score_wt(sentence, c)))

#######final func########################
# return the class with highest score for sentence
def classify(sentence):
    high_class = None
    high_score = 0
    # loop through our classes
    for c in class_words.keys():
        # calculate score of sentence for each class
        score = calculate_class_score_wt(sentence, c, show_details=False)
        # keep track of highest score
        if score > high_score:
            high_class = c
            high_score = score

    return high_class, high_score





















