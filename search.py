def search(query):
    
    obj={}
    connection = pymongo.Connection("localhost", 27017)
    db = connection['newdata']
    collection = db['collection'] 

    regex_string = '/.*' + query + '.*/'
    print regex_string
    query = db.collection.find( { $and : [ { Title : regex_string } ,{ PostTypeId : "1"}, { AnswerCount : "0"}] })
    
    for data in query:
        title = data['Title']
        Id = data['Id']
        obj = {}
        obj['Id'] = Id
        obj['Title'] = title
        print obj
    

def main():    
   
    query = 'C'
    search(query);
       
if __name__ == '__main__':
  main()
