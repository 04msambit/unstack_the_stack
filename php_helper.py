import pymongo
connection = pymongo.Connection("localhost", 27017)
db = connection['newdata']
#649980
question = db.collection.find({"Id":"649980"})
for q in question:
    title= q['Title']
print title

