import json
import re
from pymongo import MongoClient

''' Start by inserting product and category collections'''
products = [
	{
		"productName" : "shirt",
		"unitPrice" : "16.22",
		"stockCount" : "100",
	},
	{
		"productName" : "pants",
		"unitPrice" : "30.22",
		"stockCount" : "200",
	},
	{
		"productName" : "disneyplus",
		"unitPrice" : "22.99",
		"stockCount" : "999999",
	},
	{
		"productName" : "movies",
		"unitPrice" : "10",
		"stockCount" : "99999999",
	},
	{
		"productName" : "disneylandtickets",
		"unitPrice" : "50",
		"stockCount" : "9999999",
	},
	{
		"productName" : "earring",
		"unitPrice" : "300",
		"stockCount" : "100",
	},
	{
		"productName" : "wristband",
		"unitPrice" : "60",
		"stockCount" : "100",
	},
	{
		"productName" : "hairclip",
		"unitPrice" : "19.99",
		"stockCount" : "100",
	},
	{
		"productName" : "robot",
		"unitPrice" : "29.99",
		"stockCount" : "100",
	},
	{
		"productName" : "barbie",
		"unitPrice" : "39.99",
		"stockCount" : "100",
	},

]

categoryDetails = [
	{
		"category" : "clothes",
		"descrition" : "Adult and kids wearable items, typically top bottoms",
	},
	{
		"category" : "digital",
		"descrition" : "Digital products, like shows, movies, or subscription based disneyplus items",
	},	
	{
		"category" : "themepark",
		"descrition" : "Themepark sales, like tickets or annual entries for themeparks",
	},
	{
		"category" : "accessories",
		"descrition" : "Accessory items for adults and kids, like wristbands, earrings etc",
	},
	{
		"category" : "Kids playable items, adult collectables",
		"descrition" : "Accessory items for adults and kids, like wristbands, earrings etc",
	},
]


json_object = json.dumps(products, indent = 3)
#print(json_object)			#python extractCustomer.py > noSQL/shoppinCart.txt

connection_string = "mongodb://localhost:27017/bbfa-team31"
client = MongoClient(connection_string)
db = client.get_database("bbfa-team31")

collection = db.get_collection("categoryDetails")

x = collection.insert_many(categoryDetails)

for i in products:
	if i["productName"] == "shirt" or i["productName"] == "pants":
		i["category"] = x.inserted_ids[0]
	elif i["productName"] == "disneyplus" or i["productName"] == "movies":
		i["category"] = x.inserted_ids[1]
	elif i["productName"] == "disneylandtickets":
		i["category"] = x.inserted_ids[2]
	elif i["productName"] == "earring" or i["productName"] == "wristband" or i["productName"] == "hairclip":
		i["category"] = x.inserted_ids[3]
	elif i["productName"] == "robot" or i["productName"] == "barbie":
		i["category"] = x.inserted_ids[4]

collection = db.get_collection("products")
x = collection.insert_many(products)

''' Above inserts all the product and categroy objects'''
''' Below inserts all the cart orders'''

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

'''
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
'''
for i in range(1000):
	rich_documents[i]["product"] = x.inserted_ids[i%5]

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


#json_object = json.dumps(rich_documents, indent = 3)
#print(json_object)			#python extractCustomer.py > noSQL/shoppinCart.txt

connection_string = "mongodb://localhost:27017/bbfa-team31"
client = MongoClient(connection_string)
db = client.get_database("bbfa-team31")

collection = db.get_collection("shoppingCarts")

x = collection.insert_many(rich_documents)
#print(x.inserted_ids)



