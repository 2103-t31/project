import json
import re
from pymongo import MongoClient

rich_documents = []

with open("customer.sql") as customers:
	for customer in customers:
		#json document for appending to list, to insert into rich_documents
		document = {}
		arr = ["firstName", "lastName", "email", "userName"]
		#start to strip
		data = (customer.split('(')[2]).split(",")[1:]
		for i in range(len(arr)):
			# data[i] is looking at each field, strip away non alphanumeric fields now
			data[i] = re.sub(r'[^A-Za-z0-9@.]+', '', data[i])
			document[arr[i]] = data[i]
		rich_documents.append(document)

json_object = json.dumps(rich_documents, indent = 3)
print(json_object)			#python extractCustomer.py > noSQL/customers.txt

'''
connection_string = "mongodb://localhost:27017/bbfa-team31"
client = MongoClient(connection_string)
db = client.get_database("bbfa-team31")

collection = db.get_collection("customers")

x = collection.insert_many(rich_documents)
print(x.inserted_ids)
'''
