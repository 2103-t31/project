import json
import re
from pymongo import MongoClient

rich_documents = []

with open("shoppingCarts.sql") as carts:
	for cart in carts:
		#json document for appending to list, to insert into rich_documents
		document = {}
		arr = ["value", "dateCreated", "discountValue", "status", "products"]
		#start to strip
		data = (cart.split('(')[2]).split(",")[1:]
		for i in range(2):
			# data[i] is looking at each field, strip away non alphanumeric fields now
			data[i] = re.sub(r'[^0-9.\-: ]+', '', data[i])
			document[arr[i]] = data[i]

		rich_documents.append(document)

#extract purchased cart's discounted value
temp = []
with open("purchasedCart.sql") as carts:
	for cart in carts:
		document = {}
		data = (cart.split('(')[2]).split(",")[2]
		data = re.sub(r'[^0-9. ]+', '', data)
		document["datePurchased"] = data
		document["status"] = "purchased"
		temp.append(document)

for i in range(600):
	rich_documents[i].update(temp[i])

#extract abandoned cart's discount value
temp = []
with open("abandonedCart.sql") as carts:
	for cart in carts:
		document = {}
		data = (cart.split('(')[2]).split(",")[1]
		data = re.sub(r'[^0-9. ]+', '', data)
		document["datePurchased"] = data
		document["status"] = "abandoned"
		temp.append(document)

for i in range(600,1000):
	rich_documents[i].update(temp[i-600])

productContents = []
with open("contains(toextract).sql") as carts:
	for cart in carts:
		document = {}
		arr = ["prouctName", "unitPrice", "category", "quantity",]
		data = (cart.split('(')[2]).split(",")[1:]
		for i in range(len(data)):
			data[i] = re.sub(r'[^A-Za-z0-9.]+', '', data[i])
			document[arr[i]] = data[i]
		productContents.append(document)	

for i in range(1000):
	rich_documents[i]["product"] = (productContents[i])

with open("visits.sql") as carts:
	i = 0
	for cart in carts:
		#json document for appending to list, to insert into rich_documents
		document = {}
		#start to strip
		data = (cart.split('(')[2]).split(",")
		# data[i] is looking at each field, strip away non alphanumeric fields now
		deviceType = re.sub(r'[^A-Za-z]+', '', data[1])
		marketC = re.sub(r'[^A-Za-z]+', '', data[4])
		rich_documents[i]["deviceType"] = (deviceType)
		rich_documents[i]["mChannels"] = (marketC)
		i += 1

f = open("noSQL/customers.json")
data = json.load(f)

for i in range(len(data)):
	rich_documents[i]["customerDetails"] = data[i]


json_object = json.dumps(rich_documents, indent = 3)
#print(json_object)			#python extractCustomer.py > noSQL/shoppinCart.txt

connection_string = "mongodb://localhost:27017/bbfa-team31"
client = MongoClient(connection_string)
db = client.get_database("bbfa-team31")

collection = db.get_collection("shoppingCarts")

x = collection.insert_many(rich_documents)
#print(x.inserted_ids)

