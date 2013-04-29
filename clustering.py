import sys
import random
import glob
import collections
import re
import json
import math
import operator
import string
import random
import pymongo
from sklearn.cluster import KMeans
from time import time ,clock

finalClustDict=collections.defaultdict(dict)
kList=[]
rssList=[]
def read():
 	global finalClustDict
 	rows = [] #we'll use this array to store all the questions we find in mongodb
 	tagDict={}
 	counter = 0
 	alpha=0.5
 	beta=0.5
 	tagList=[]
 	connection = pymongo.Connection("localhost", 27017)

 	db = connection['newdata']
 	#test_dictionary = db['test_dictionary']
 	count = 0
 	for question in db.test_dictionary.find():
 		rows.append(question)
 	 	
 	for row in rows:
 		count+=1
 	 	print count	
 		tempDict={}
 		for term in row['Term_Body']:
 			if term in row['Term_Title']:
 				tempDict[term]=alpha*row['Term_Body'][term]+beta*row['Term_Title'][term]
 			else:
 				tempDict[term]=row['Term_Body'][term]
 		
 		for term in row['Term_Title']:
 			if not(term in row['Term_Title']):
 				tempDict[term]=row['Term_Title'][term]
 		
 		tags=re.split('>|<',row['Tags'])
 		for tag in tags:
 			f=0
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

 				
 				if tag in tagDict:
 					tagDict[tag][row['Id']]=tempDict.copy()
 				else:
 					tagDict[tag]={}
  					tagDict[tag][row['Id']]=tempDict.copy()
 	print "final: "+str(count)
	km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1,verbose=1)
 	for tag in tagList:	
 		if len(tagDict[tag]) < 100 :
 			print "cluster 1"
			km.fit(X)
 		else:
 			print "cluster 6"
 			km.fit(X)
 	#for tag in finalClustDict:
 	 #	print tag+" : "
 	#	for id in finalClustDict[tag]: 
 	#		print str(id) +" - "+str(finalClustDict[tag][id][0])
 	#insert_in_db()

 	#	print "###################"		
 	#	for t in tagDict:
 	#		for docId in tagDict[t]:
 	#			print t+":"+docId
 		#print len(tempDict)
 		
 	#create_cluster(1,tagDict["php"],len(tagDict["php"]),"php")

def insert_in_db():
 	global finalClustDict 	
 	connection = pymongo.Connection("localhost", 27017)
 	db = connection['newdata']
 	clustertable = db['clustertable']
 	for tag in finalClustDict:
 		print tag
 		db.clustertable.insert({ "tag":tag ,"clusterDict" : finalClustDict[tag]})



def calcNewCentroid(clustDict,tfDict):
 	centroid=[]
 	for clusterid in clustDict:
 		temp={}
 		for docId in clustDict[clusterid]:
 			temp=calcVectorSum(temp,tfDict[docId],len(clustDict[clusterid])) 	
 		centroid.append(temp)
 
 	return centroid
	
def calcVectorSum(vec1,vec2,l):
 	if len(vec1)==0:
 		return vec2
 	if len(vec2)==0:
 		return vec1

 	vec3={}
 	for term in vec1:
 		if term in vec2:
 			vec3[term]=(vec1[term]+vec2[term])/float(l)
 		else:
 			vec3[term]=vec1[term]/float(l)

 	for term in vec2:
 		if not(term in vec1):
 			vec3[term]=vec2[term]/float(l)
 	return vec3


def main():

#  if len(sys.argv) <2:
 # 	print 'usage: ./bt.py file-to-read words-to-search'
  #	sys.exit(1)

  start=time()	
  read()
  print "Time Taken:",(time()-start)
  

if __name__ == '__main__':
  main()
