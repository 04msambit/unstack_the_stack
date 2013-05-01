import pymongo
import sys
def search(query):
    
    obj={}
    connection = pymongo.Connection("localhost", 27017)
    db = connection['newdata']
    collection = db['collection'] 

    query = db.collection.find({"$and":[{"Title": {"$regex": query}},{ 'PostTypeId' : '1'}, { 'AnswerCount' : '0'}] })

    
    ctr = 0
    counter=0
    for data in query:
        post_id = data['PostTypeId']
        answer_count = data['AnswerCount']
        if ( ctr > 15):
           break        
        
       	ctr+=1
	title = data['Title']
        Id = data['Id']
        obj = {}
        obj['Id'] = Id
        obj['Title'] = title
        
        print obj
    

def main(argv):    
   
    query = sys.argv[1]
    search(query);
       
if __name__ == '__main__':
  main(sys.argv[1:])
