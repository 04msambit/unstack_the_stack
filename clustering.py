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
 	for tag in tagList:	
 		if len(tagDict[tag]) < 100 :
 			create_cluster(1,tagDict[tag],len(tagDict[tag]),tag)
 		else:
 			create_cluster(6,tagDict[tag],len(tagDict[tag]),tag)
 	print count
 	for tag in finalClustDict:
 	 	print tag+" : "
 		for id in finalClustDict[tag]: 
 			print str(id) +" - "+str(finalClustDict[tag][id][0])
 					tagDict[tag][row['Id']]=tempDict.copy()

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
 		db.clustertable.insert({ "tag":tag ,"clusterDict" : finalClustDict[tag]})


def create_cluster(k,tfDict,N,tag):

 	global kList
 	global rssList
 	global finalClustDict

 	ls1=[]
 	centroid_list=[]
 	clustersDict=collections.defaultdict(dict)
	ls=random.sample(range(N),k)

 	if not(tag in finalClustDict):
 		finalClustDict[tag]={}

 	for id in tfDict:
 		ls1.append(id)

 	for i in range(k):
 		centroid_list.append(tfDict[ls1[i]])
 	
 	count=0	
 	oldcluster=collections.defaultdict(dict)
 	flag=0
 	kList.append(k)
 	while True:
 		flag=0
 		count+=1
 		if count==100:
 			break

 		oldcluster=clustersDict.copy()
 		for i in range(k):
 			clustersDict[i]=[]	
 		for id in tfDict:
 			eucList=[]
 			for i in range(k):
 				eucList.append(calcEuclidean(tfDict[id],centroid_list[i]))

 			clustersDict[min(eucList)].append(id)	
 		
 	 	centroid_list=calcNewCentroid(clustersDict,tfDict)

 		for clusterid in clustersDict:
 			if clustersDict[clusterid]==oldcluster[clusterid]:
 				flag=1
 				continue
 			else:
 				break
 	
 		if flag ==1:
 			#print "clustered"
 			break
	#print tag
 	for id in clustersDict:
 		finalClustDict[tag][id]=[clustersDict[id]]
 		finalClustDict[tag][id].append(centroid_list[id])
 	#rssList.append(calcRSS(clustersDict,centroid_list))
 	#print str(k)+": Purity- "+str(calcPurity(clustersDict))
 	#print str(k)+": RI- "+str(calcRandIndex(clustersDict))

def calcRandIndex(clusterDict):
 	global classInClusterDict
 	TPplusFP=0.0
 	TNplusFN=0.0
 	TP=0.0
 	FP=0.0
 	FN=0.0
 	TN=0.0
 	previteratedList=[]
 	for clusterid in clusterDict:
 		TPplusFP=TPplusFP+nC2(len(clusterDict[clusterid]))
 		for className in classInClusterDict[clusterid]:
 			TP=TP+nC2(classInClusterDict[clusterid][className])

 		for clustid in clusterDict:
 			if not(clustid in previteratedList) and clustid != clusterid:
 				for className in classInClusterDict[clusterid]:
 					for classN in classInClusterDict[clustid]:
 						if className !=classN:
 				
		 					TN=TN+classInClusterDict[clusterid][className] *classInClusterDict[clustid][classN]
# 							print str(clusterid)+"-"+str(clustid)+"-"+ str(classInClusterDict[clusterid][className])+"-"+str(classInClusterDict[clustid][classN])+"-"+str(TN)
						
 		previteratedList.append(clusterid)

 	FP=TPplusFP-TP
 	num=TP+TN
 	den=nC2(totalNoDocuments)
 	return 100*num/float(den)

def nC2(n):
 	if n>=2:
 		return n*(n-1)/float(2)
 	else:
 		return 0.0

def plotGraph(x,y):
 	print x 
 	print y
	pylab.figure()
	pylab.plot(x, y, "*")
	pylab.show()

def calcPurity(clusterDict):
        global docClass
        global totalNoDocuments
 	global classInClusterDict
        purity=0.0
        for clusterid in clusterDict:
 		classInClusterDict[clusterid]={}

                for id in clusterDict[clusterid]:
                        if docClass[id] in classInClusterDict[clusterid]:
                                classInClusterDict[clusterid][docClass[id]]+=1
                        else:
                                classInClusterDict[clusterid][docClass[id]]=1
                sorted_x=sorted(classInClusterDict[clusterid].items(),key=operator.itemgetter(1))
                purity=purity+100*sorted_x[-1][1]/float(totalNoDocuments)
        return purity


def calcRSS(clustDict,centroid_list):
 	RSS={}
 	sum=0.0
 	for clusterid in clustDict:
 		for docId in clustDict[clusterid]:
 			sum=sum+math.pow(calcEuclidean(tfDict[docId],centroid_list[clusterid]),2) 
 		#RSS[clusterid]=sum
 	return sum

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

def min(valList):
 	min=valList[0]
 	index=0
 	for i in range(len(valList)):
 		if valList[i]<=min:
 			min=valList[i]
 			index=i

 	return index
def calcEuclidean(vec1,vec2):
 	diff=0.0
 	for term in vec1:
 		if term in vec2:
 			diff=diff+(vec1[term]-vec2[term])*(vec1[term]-vec2[term])
 		else:
 			diff=diff+vec1[term]*vec1[term]

 	for term in vec2:
 		if not(term in vec1):
 			diff=diff+vec2[term]*vec2[term]
 
 	return math.sqrt(diff)

def main():

#  if len(sys.argv) <2:
 # 	print 'usage: ./bt.py file-to-read words-to-search'
  #	sys.exit(1)

  start=time()	
  read()
  print "Time Taken:",(time()-start)
  

if __name__ == '__main__':
  main()
