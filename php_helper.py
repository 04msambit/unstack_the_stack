import pymongo
connection = pymongo.Connection("localhost", 27017)
db = connection['newdata']
#649980
question = db.result_cache.find()
for q in question:
    q_id= q['Unanswered_Question_Id']
    question = db.collection.find({"Id":q_id})
    for data in question:
	title = data['Title']
    print data

