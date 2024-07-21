import mysql.connector

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'keepitlow',
    'database': 'chatbot'
}

# Create database connection
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection
