import mysql.connector
import json

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'keepitlow',
    'database': 'chatbot'
}

# Read JSON data from file
try:
    with open('questions.json', 'r') as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"JSON Decode Error: {e}")
    exit()

# Connect to the database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Define the insert query
insert_query = """
INSERT INTO questions (question, answer, level, parent)
VALUES (%s, %s, %s, %s)
"""

# Insert data from JSON
for item in data:
    question = item.get('question')
    answer = item.get('answer')
    level = item.get('level', None)
    parent = item.get('parent', None)
    cursor.execute(insert_query, (question, answer, level, parent))

# Commit the transaction
connection.commit()

print("Data inserted successfully!")

# Close connection
cursor.close()
connection.close()
