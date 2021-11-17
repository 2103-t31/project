# Project

# How to run

```bash
# Create a virtual env
python3 -m venv team31-bbfa

# Source the virtual env, on windows:
team31-bbfa\Scripts\activate

# On Unix, MacOS
source team31-bbfa/bin/activate

# Install the requirements
python -m pip install -r requirements.txt

# Run the app
python app.py

```

# To create or reset the database,

```bash
# Delete old sqlite file DB
rm bbfa-db.db
# Use script to create new sqlite file DB
python db.py

```

# NoSQL portion

# Start MongoDB locally
```bash
# cd to your local MongoDB server (C:\Program Files\MongoDB\Server\5.0\bin)
cd $(PATH)
# Start local mongoDB server
mongod
```

# Can use MongoCompass to view your db and collections
`Open MongoDB Compass -> Fill in connection fields individualy -> follow image -> connect`
![Test Image 1](images/mongodb.png)

