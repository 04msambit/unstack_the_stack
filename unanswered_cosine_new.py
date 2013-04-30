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
    
    sum_square_query_body=0.0
    sum_square_query_title=0.0

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
    
    list_ids = db.result_cache.find({"Unanswered_Question_Id":query_id})
    
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

    	for test_obj in query:
            query_body=test_obj["Term_Body"]
            query_title=test_obj["Term_Title"]
            query_tags = test_obj["Tags"]
      
        
        for kk in query_body:
            sum_square_query_body += float(query_body[kk] * query_body[kk])
    
    	sum_square_query_body=float(math.sqrt(sum_square_query_body));    
    
    	for kk in query_title:
            sum_square_query_title += query_title[kk] * query_title[kk]

    	sum_square_query_title=float(math.sqrt(sum_square_query_title));

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

        tagList=[]
        query_lst=re.split('>|<',query_tags)
        
 	for tag in query_lst:
 		if tag != "" :
        		tag=tag.lower()
 			if tag == "c" or tag == "c++" or tag == "c#":
 				if not(tag in tagList):
 					tagList.append(tag)
 			else :
 				if "java" in tag:
					 tag="java"
 				if ".net" in tag or "asp" in tag :
					tag=".net"
 				if "sql" in tag :
 					tag="mysql"
 			if not(tag in tagList):
 				tagList.append(tag)
        
        
        t_list = search(query_id,merge_dict,tagList)
 	
        search_list=[]
	for each in t_list:
 		search_list.append(each.encode('ascii'))
 		
        
    	#query_question = db.test_dictionary.find() # We will have to chage it to the List of Ids Based on Set of Clustering Ids
	    	
        
                   
        query_question= db.test_dictionary.find({"Id":{"$in":search_list}})

               
        question_count = 0
    	list_for_heap = []
    	for obj in query_question:
        	question_count +=1
        	row_id = obj["Id"]  
        	question_body=obj["Term_Body"]
        	question_title=obj["Term_Title"]
        	question_tags = obj["Tags"]

		                 

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
		
		if(question_count < 10 ):
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
        	obj = {}
		obj['Id'] = query_obj["Id"]
		obj['Title'] = query_obj["Title"]
  		print obj

    	print '\nMatching Questions..!!!!\n'

    	cache_list=[]


    	for element in list_for_heap:
        	id_value=element["id"] 
                id_value.encode("ascii")
        # Forming a Cache List which will be pushed into Dictionary 
        	cache_list.append(id_value)
     
        	db_result = db.collection.find({"Id":id_value})
        	for result_obj in db_result:
            		obj = {}
			obj['Id'] = result_obj["Id"]
			obj['Title'] = result_obj["Title"]
  			print obj
                
        db.result_cache.insert({"Unanswered_Question_Id":query_id , "Answered_Question_List":cache_list})

    else:
        
        query = db.collection.find({"Id":query_id})
       
    	for query_obj in query:
        	print '\nUnanswered Question:'
        	obj = {}
		obj['Id'] = query_obj["Id"]
		obj['Title'] = query_obj["Title"]
  		print obj
                
    	print '\nMatching Questions..!!!!\n'

        for id_result in result_list:
            db_result = db.collection.find({"Id":id_result})
            for result_obj in db_result:
		obj = {}
		obj['Id'] = result_obj["Id"]
		obj['Title'] = result_obj["Title"]
  
                print obj
                #print'\n'  
       
         
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
        
        query = db.clustertable.find({"tag":every_tag})
        
        for query_obj in query:
            cluster_dict=query_obj["clusterDict"]
        
        for i in cluster_dict:
            for id in cluster_dict[i][0]:
                if id not in result_list:
                   result_list.append(id)
       
	'''if every_tag == "c#":
 		for i in cluster_dict:
 			print str(i)+" :" +str(len(cluster_dict[i][0]))
	quit()
        for key in cluster_dict:
            score_value = cosine_value(vector,cluster_dict[key][1],sum_value)
            if key not in map_dict:
               map_dict[key] = score_value
               
            dist_list.append(score_value)

        min_score = min(dist_list)
        
        for key in map_dict:
            if ( min_score == map_dict[key] ):
               required_key= key
        print required_key
 	print every_tag
 	print cluster_dict[required_key]	
 	for id in cluster_dict[required_key][0]:
                if id not in result_list:
 		   	result_list.append(id)            
	print "rea",
	print result_list
	quit()'''
    
    
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
        denominator+=float(question[key_dic] * question[key_dic])
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

    ques_id = sys.argv[1]    
    read(ques_id);

    '''connection = pymongo.Connection("localhost", 27017)

    db = connection['newdata']
    collection = db['collection']
    quer=db.collection.find({"PostTypeId":"1","AnswerCount":"0"})
    
    for query_obj in quer:
        ques_id=query_obj["Id"] 
        read(ques_id); '''

       
if __name__ == '__main__':
  main(sys.argv[1:])
