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



def main():    
    read();
       
if __name__ == '__main__':
  main()
