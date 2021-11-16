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
