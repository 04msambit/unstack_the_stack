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


def read(query_id):
    
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
    
    # We will see if the Question Id is present inside the Cluster 
    
    list_ids = db.result_cache.find({"Id":query_id})
    
    counter_value = 0
    for each_object_value in list_ids:
        counter_value+=1
        result_list = each_object_value["Answered_Question_List"]
    
    
    if(counter_value==0):    

    	query = db.test_dictionary.find({"Id":query_id}) # We will have to chage it to the List of Ids Based on Set of Clustering Ids 

    	query_body={}
    	query_title={}
    	question_body={}
    	question_title={}
        query_tags =""

    	for obj in query:
        	query_body=obj["Term_Body"]
        	query_title=obj["Term_Title"]
                query_tags = obj["Tags"]
      
    

        for kk in query_body:
           if kk in idf_dictionary_body:
                     
              idf_value = idf_dictionary_body[kk]    # We are getting the idf value for that term
           #print idf_value
           else:
              idf_value =0
           query_body[kk] = query_body[kk] * idf_value
           sum_square_query_body += query_body[kk] * query_body[kk]
    
    	sum_square_query_body=math.sqrt(sum_square_query_body);    
    
    	for kk in query_title:
        	if kk in idf_dictionary_title:

           	   idf_value = idf_dictionary_title[kk]    # We are getting the idf value for that term
                else:
                   idf_value =0
                query_title[kk] = query_title[kk] * idf_value
                sum_square_query_title += query_title[kk] * query_title[kk]

    	sum_square_query_title=math.sqrt(sum_square_query_title);

    # We will write the code to Calculate Cosine Similarity Here

        # Form Merged Dictionary
        merge_dict={}
        for kk in query_body:
            if kk in query_title:
               if kk not in merge_dict:
                  merge_dict[kk]= float( 0.5 * query_title[kk] ) * float ( 0.5 * query_body[kk] )
            else:
               if kk not in merge_dict:
                  merge_dict[kk]= float( 1.0 * query_body[kk] )
   
        for kk in query_title:
            if kk not in merge_dict:
                  merge_dict[kk]= float( 1.0 * query_title[kk] )

        
        query_lst=re.split('>|<',query_tags)
        search_list = search(query_id,merge_dict,query_lst)


    	query_question = db.test_dictionary.find() # We will have to chage it to the List of Ids Based on Set of Clustering Ids
    	            

        question_count = 0
    	list_for_heap = []
    	for obj in query_question:
        	question_count +=1
        	row_id = obj["Id"]  
        	question_body=obj["Term_Body"]
        	question_title=obj["Term_Title"]
        	question_tags = obj["Tags"]
    
    
		if sum_square_query_title == 0:
		   print "abcd"

		

		title_cosine_value = cosine_value(query_title,question_title,sum_square_query_title)
		body_cosine_value = cosine_value(query_body,question_body,sum_square_query_body)
		tag_value= tag_similarity_calc(query_tags,question_tags)       
		#Based on this score we will decide how to weigh them and use
		tag_weight = 0.0
		if(len(query_tags)!=0):
		  lst_query=re.split('>|<',query_tags)
		  lst_query = list(filter(None, lst_query))
		  original_tag_value = len(lst_query)
		  
		  tag_weight = tag_value/ float(original_tag_value) * 0.50

		title_weight = float(title_cosine_value) * 0.30        
		body_weight = float(title_cosine_value) * 0.20

		

		aggregate_weight = tag_weight+title_weight+body_weight
		
		if(question_count < 5 ):
		  list_for_heap.append({"id":row_id,"weight":aggregate_weight})
		else:
		  #new_list = sorted(list_for_heap, key=lambda k: k['weight'],reverse='True') 
		  list_for_heap.sort(key=operator.itemgetter('weight'),reverse=True)
		  chk_value = list_for_heap[-1]["weight"]
		  if (aggregate_weight > chk_value):
		     list_for_heap[-1]={"id":row_id,"weight":aggregate_weight}
      
    

	query = db.collection.find({"Id":query_id})
       
    	for query_obj in query:
        	print '\nUnanswered Question:'
        	print 'Title: ',  
        	print query_obj["Title"]

    	print '\nMatching Questions..!!!!\n'   

    	cache_list=[]

    	for element in list_for_heap:
        	id_value=element["id"] 
        
        # Forming a Cache List which will be pushed into Dictionary 
        	cache_list.append(id_value)
     
        	db_result = db.collection.find({"Id":id_value})
        	for result_obj in db_result:
            		print 'Title: ',
            		print result_obj["Title"] 
            		print'\n'

        db.result_cache.insert({"Unanswered_Question_Id":query_id , "Answered_Question_List":cache_list})

    else:
    
        for id_result in result_list:
            db_result = db.collection.find({"Id":id_result})
            for result_obj in db_result:
                print 'Title: ',
                print result_obj["Title"]
                print'\n'
 

    
    return

def search(id_query,vector,tag_list):
     
    sum_value = 0.0
    map_dict={}
    result_list=[]
    dist_list=[]
    map_dict={}
    cluster_dict={}

    for key_value in vector:
        sum_value+= float ( vector[key_value] ) * float( vector[key_value])
    
    sum_value = math.sqrt(sum_value);


    connection = pymongo.Connection("localhost", 27017)

    db = connection['newdata']
    clustertable = db['clustertable']


    for every_tag in tag_list:

        query = db.clustertable.find({"tag":ever_tag})
        for query_obj in query:
            cluster_dict=query_obj["clusterDict"]

        for key in cluster_dict:
            score_value = cosine_value(vector,cluster_dict[key][1],sum_value)
            if key not in map_dict:
               map_dict[key] = score_value
               
            dist_list.append(score_value)

        min_score = min(dist_list)
        
        for key in map_dict:
            if ( min_score == map_dict[key] ):
               required_key= key
        
        result_list.append(cluster_dict[key][0])            

    return result_list


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

def main(argv):

    connection = pymongo.Connection("localhost", 27017)

    db = connection['newdata']
    collection = db['collection']
    quer=db.collection.find({"PostTypeId":"1","AnswerCount":"0"})
    
    for query_obj in quer:
        ques_id=query_obj["Id"] 
        read(ques_id);
       
if __name__ == '__main__':
  main(sys.argv[1:])
