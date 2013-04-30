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



def read():
    
    questions = [] #we'll use this array to store all the questions we find in mongodb
    questionsd = []
    
    sum_square_query_body=0
    sum_square_query_title=0

    connection = pymongo.Connection("localhost", 27017)
   
    db = connection['newdata']
    collection = db['collection']
    idf_dictionary_body_collection = db['idf_dictionary_body']
    idf_dictionary_title_collection = db['idf_dictionary_title']
    


    idf_dictionary_body = idf_dictionary_body_collection.find()
    idf_dictionary_title = idf_dictionary_title_collection.find()

    count = 0
    question_xml = db.collection.find({"Id":"354405"}) # We will have to chage it to the search query or selected id   
    
    for result_object in question_xml:
        
        count+=1
        question_body=result_object["Body"]
        question_title=result_object["Title"]
    
    print question_body
    print question_title	 


    if(question_body!=None):
      question_body_list = word_preprocessing(question_body)
    else:
      question_body_list =[]

    if(question_title!=None):
      question_title_list = word_preprocessing(question_title)
    else:
      question_title_list =[]
    
    
    query_tf_body_dict = collections.defaultdict(float)
    query_tf_title_dict = collections.defaultdict(float)
    
    # We will create a trem frequency dictionary here
	
        
    for wrd in question_body_list:
      if  wrd not in query_tf_body_dict:
          query_tf_body_dict[wrd]=1
      else:
          query_tf_body_dict[wrd]+=1

    for wrd in question_title_list:
      if  wrd not in query_tf_title_dict:
          query_tf_title_dict[wrd]=1
      else:
          query_tf_title_dict[wrd]+=1


    # Now we will convert it to log form

    for ky in query_tf_title_dict:
        value = query_tf_title_dict[ky]
        query_tf_title_dict[ky]=1+float(math.log(value,2))

    for ky in query_tf_body_dict:
        value = query_tf_body_dict[ky]
        query_tf_body_dict[ky]=1+float(math.log(value,2))


    
    for kk in query_tf_body_dict:
        if kk in idf_dictionary_body:
          
           idf_value = idf_dictionary_body[kk]    # We are getting the idf value for that term
        else:
            idf_value =0
        query_tf_body_dict[kk] = query_tf_body_dict[kk] * idf_value
        sum_square_query_body += query_tf_body_dict[kk] * query_tf_body_dict[kk]
    
    sum_square_query_body=math.sqrt(sum_square_query_body);    
    
    for kk in query_tf_title_dict:
        if kk in idf_dictionary_title:

           idf_value = idf_dictionary_title[kk]    # We are getting the idf value for that term
        else:
            idf_value =0
        query_tf_title_dict[kk] = query_tf_title_dict[kk] * idf_value
        sum_square_query_title += query_tf_title_dict[kk] * query_tf_title_dict[kk]

    sum_square_query_title=math.sqrt(sum_square_query_title);

    # We will write the code to Calculate Cosine Similarity Here

    print "unanswered tfidf dict"        
    query_question = db.term_dictionary.find({"Id":"354405"}) # We will have to chage it to the List of Ids Based on Set of Clustering Ids 
			    
    for obj in query_question:
        question_body=obj["Term_Body"]
        question_title=obj["Term_Title"]

   
    title_cosine_value = cosine_value(query_tf_title_dict,question_title,sum_square_query_title)
    body_cosine_value = cosine_value(query_tf_body_dict,question_body,sum_square_query_body)
     
    # Based on this score we will decide how to weigh them and use

    print 'Done'  
   
    return

def cosine_value(query,question,denom_value):
    
    for key_dic in question:
        denominator+=question[key_dic] * question[key_dic]
    for kl in query:
        if kl in question:
           sum_val+=question[kl]*query[kl]
        else:
           sum_val+=0

        mult_denominator= float( math.sqrt(denominator) )
        
        if(mult_denominator!=0):      
          score_doc=sum_val/float (denom_value * math.sqrt(denominator))

    return score_doc


def word_preprocessing(word):
 return re.findall(r"[\w]+", word.lower())



def main():    
    read();
       
if __name__ == '__main__':
  main()
