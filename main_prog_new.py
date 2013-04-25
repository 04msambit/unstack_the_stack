import sys
import json
import simplejson
import difflib
import re
import collections
import math
import numpy
import operator
import random
import pymongo
import time

idf_dictionary_title=collections.defaultdict(float)
idf_dictionary_body=collections.defaultdict(float)

d_title=collections.defaultdict(float)
d_body=collections.defaultdict(float)
d_t=collections.defaultdict(float)
d_b=collections.defaultdict(float)
tags_d=collections.defaultdict(float)

#term_dict=collections.defaultdict()

def read():
    
    questions = [] #we'll use this array to store all the questions we find in mongodb
    questionsd = []

    counter = 0
    connection = pymongo.Connection("localhost", 27017)
   
    db = connection['newdata']
    collection = db['collection']
    count = 0
    for question in db.collection.find():                 
        questions.append(question) 
          
    for test in questions:
     counter+=1
     if(counter < 100):  
	if test['PostTypeId'] == '1':
				
                rowId = test['Id']
                
                if 'Tags' in test:
                    tags  = test['Tags']
                else:
                    tags = None
		
                count+=1
		title_text = test['Title'] 
                body_text = test['Body']
		
		wordlist1=word_preprocessing(title_text)
                wordlist2=word_preprocessing(body_text)

		set_list1 = set(wordlist1)
                set_list2 = set(wordlist2)

		for word in set_list1:
		    if idf_dictionary_title.has_key(word):
		       idf_dictionary_title[word]+=1;
		    else:
		       idf_dictionary_title[word]=1;

                for word in set_list2:
                    if idf_dictionary_body.has_key(word):
                       idf_dictionary_body[word]+=1;
                    else:
                       idf_dictionary_body[word]=1;


		# We will create a term frequency dictionary here
		if rowId not in d_title:
			d_title[rowId] = {}
		if rowId not in d_body:
                        d_body[rowId] = {}
                
                if rowId not in tags_d:
                        tags_d[rowId] = tags
            


		for wrd in wordlist1:
		    if  wrd not in d_t:
			d_t[wrd]=1
		    else:
			d_t[wrd]+=1

                for wrd in wordlist2:
                    if  wrd not in d_b:
                        d_b[wrd]=1
                    else:
                        d_b[wrd]+=1

 
		for ky in d_t:
		     value = d_t[ky]
		     d_t[ky]=1+float(math.log(value,2))

                for ky in d_b:
                     value = d_b[ky]
                     d_b[ky]=1+float(math.log(value,2))
		d_title[rowId] = d_t
		d_body[rowId] = d_b	

    for key in idf_dictionary_title:
        val = count/float(idf_dictionary_title[key])
        idf_dictionary_title[key]=math.log(val,2)


    for key in idf_dictionary_body:
        val = count/float(idf_dictionary_body[key])
        idf_dictionary_body[key]=math.log(val,2)

    print 'The length of d_title is ',
    print len(d_title)

        
    lst=[]
    test_dictionary = db['test_dictionary']	
    ctr = 0
    for key in d_title:
        
        ctr+=1
	for kk in d_title[key]:
            idf_value = idf_dictionary_title[kk]    # We are getting the idf value for that term
            raw_term_frequency = d_title[key][kk]
            d_title[key][kk] = float(d_title[key][kk]) * float(idf_value)
           
        for word in d_body[key]:
         	idf_value = idf_dictionary_body[word]    # We are getting the idf value for that term
		raw_term_frequency = d_body[key][word]
		d_body[key][word] = float(d_body[key][word]) * float(idf_value)
	

        #Inserting into DB
       
        print ctr 
        db.test_dictionary.insert( { "Id":key ,"Tags": tags_d[key] , "Term_Body" : d_body[key] , "Term_Title" : d_title[key] })
	

    # We will insert into a mongo db

    db.idf_dictionary_title_test.insert(idf_dictionary_title)
    db.idf_dictionary_body_test.insert(idf_dictionary_body)

    return

def word_preprocessing(word):
 return re.findall(r"[\w]+", word.lower())


def main():    
    read();
       
if __name__ == '__main__':
  main()
