from pymongo import MongoClient

client = MongoClient("mongodb+srv://root:1234@cluster0.pzy0t.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# 만약에 안되면 뒤에 tls = True, tlsAllowInvalidCertificates=True 를 추가해라!

db = client.test

list = db.mydata
list.insert_one({"data":"test", "fwe":"few", "dict":{"test":"sssddd"}})