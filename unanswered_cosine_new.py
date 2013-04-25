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
import heapq


def read():
    
    questions = [] #we'll use this array to store all the questions we find in mongodb
    questionsd = []
    
    sum_square_query_body=0
    sum_square_query_title=0

    connection = pymongo.Connection("localhost", 27017)
   
    db = connection['newdata']
    collection = db['collection']
    idf_dictionary_body_collection = db['idf_dictionary_body_test']
    idf_dictionary_title_collection = db['idf_dictionary_title_test']
    


    idf_dictionary_body = idf_dictionary_body_collection.find_one()
    idf_dictionary_title = idf_dictionary_title_collection.find_one()

    
    #print idf_dictionary_title
   

    count = 0
    
    query = db.test_dictionary.find({"Id":"354449"}) # We will have to chage it to the List of Ids Based on Set of Clustering Ids 

    query_body={}
    query_title={}
    question_body={}
    question_title={}


    for obj in query:
        query_body=obj["Term_Body"]
        query_title=obj["Term_Title"]
        query_tags = obj["Tags"]
      
    

    for kk in query_body:
        if kk in idf_dictionary_body:
                     
           idf_value = idf_dictionary_body[kk]    # We are getting the idf value for that term
           #print idf_value
def tag_similarity_calc(query_tag,question_tag):
    
    query_list=re.split('>|<',query_tag)
    question_list=re.split('>|<',question_tag)
    counter = 0
    for every_elem in query_list:
        if every_elem != '':
           if ( every_elem in question_list):
              counter+=1
    
    return counter


def cosine_value(query,question,denom_value):
    #print query
    #print "q"
    #print question
    score_doc=0.0
    sum_val = 0.0
    denominator = 0.0   
    for key_dic in question:
        denominator+=question[key_dic] * question[key_dic]
	#print denominator
    for kl in query:
        if kl in question:
           sum_val+=question[kl]*query[kl]
        else:
           sum_val+=0

        mult_denominator= float( math.sqrt(denominator) )
        
        if(mult_denominator!=0):      
          score_doc=sum_val/float (denom_value * mult_denominator)

    return score_doc

def tag_similarity_calc(query_tag,question_tag):
    
    query_list=re.split('>|<',query_tag)
    question_list=re.split('>|<',question_tag)
    counter = 0
    for every_elem in query_list:
        if every_elem != '':
           if ( every_elem in question_list):
              counter+=1
    
    return counter


def cosine_value(query,question,denom_value):
    #print query
    #print "q"
    #print question
    score_doc=0.0
    sum_val = 0.0
    denominator = 0.0   
    for key_dic in question:
        denominator+=question[key_dic] * question[key_dic]
	#print denominator
    for kl in query:
        if kl in question:
           sum_val+=question[kl]*query[kl]
        else:
           sum_val+=0

        mult_denominator= float( math.sqrt(denominator) )
        
        if(mult_denominator!=0):      
          score_doc=sum_val/float (denom_value * mult_denominator)

    return score_doc

def word_preprocessing(word):
 return re.findall(r"[\w]+", word.lower())

def word_preprocessing(word):
 return re.findall(r"[\w]+", word.lower())


def main():    
    read();
       
if __name__ == '__main__':
  main()
