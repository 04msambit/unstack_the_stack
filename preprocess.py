import urllib
import pymongo
from collections import defaultdict
from xml.parsers import expat
import xml.etree.ElementTree as xml
#parser = xml.XMLParser(0,None,'UT')
#parser = etree.XMLParser(recover=True)


datadict = defaultdict()
tree = xml.parse('/home/gaurav/670/Split_XML/Posts.xml.007')
root = tree.getroot()

connection = pymongo.Connection("localhost", 27017)
db = connection['newdata']
collection = db['collection']
#db.dropDatabase()
counter=0
for child in root:
    counter+=1
    if 'Id' in child.attrib:
	Id = child.attrib['Id']
    else:
	Id = None
    if 'PostTypeId' in child.attrib:
	PostTypeId = child.attrib['PostTypeId']
    else:
	PostTypeId = None
    if 'Body' in child.attrib:
	Body = child.attrib['Body']
    else:
	Body = None
    if 'Title' in child.attrib:
	Title = child.attrib['Title']
    else:
	Title = None
    if 'Score' in child.attrib:
	Score = child.attrib['Score']
    else:
	Score = None
    if 'ParentId' in child.attrib:
	ParentId = child.attrib['ParentId']
    else:
	ParentId = None
    if 'AcceptedAnswerId' in child.attrib:
	AcceptedAnswerId = child.attrib['AcceptedAnswerId']
    else:
	AcceptedAnswerId = None
    if 'Tags' in child.attrib:
        Tags = child.attrib['Tags']
    else:
        Tags = None
    if 'AnswerCount' in child.attrib:
        AnswerCount = child.attrib['AnswerCount']
    else:
        AnswerCount = None
         
    db.collection.insert( {"Id":Id ,"PostTypeId": PostTypeId,"Body": Body,
"Title": Title,
"Score": Score,
"ParentId": ParentId,
"AcceptedAnswerId": AcceptedAnswerId,
"Tags": Tags,
"AnswerCount" : AnswerCount
})
    


    

