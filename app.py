from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
import json

app = Flask(__name__)

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
    return mysql.connector.connect(**db_config)

# Insert Data Route
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        level = request.form['level']
        parent = request.form['parent']

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            sql = "INSERT INTO questions (question, answer, level, parent) VALUES (%s, %s, %s, %s)"
            values = (question, answer, level, parent)
            cursor.execute(sql, values)
            connection.commit()
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('insert'))
    return render_template('insert.html')

# Select Data Route
@app.route('/select', methods=['GET', 'POST'])
def select():
    if request.method == 'POST':
        level = request.form['level']
        parent = request.form['parent']

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            sql = "SELECT * FROM questions WHERE level = %s AND parent = %s"
            values = (level, parent)
            cursor.execute(sql, values)
            results = cursor.fetchall()
            return jsonify(results)
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            connection.close()

    return render_template('select.html')

# Route to populate database from JSON file
@app.route('/populate')
def populate():
    with open('Sample Question Answers.json') as f:
        data = json.load(f)

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        insert_query = """
        INSERT INTO questions (question, answer, level, parent)
        VALUES (%s, %s, %s, %s)
        """

        for item in data:
            question = item['question']
            answer = item['answer']
            level = item.get('level', 1)
            parent = item.get('parent', None)
            cursor.execute(insert_query, (question, answer, level, parent))

        connection.commit()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

    return "Database populated successfully!"

# Chat Route
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data['message']
    level = data.get('level', None)
    parent = data.get('parent', None)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Execute the query to find the answer
        query = "SELECT answer FROM questions WHERE question=%s"
        cursor.execute(query, (user_message,))
        
        # Fetch the result
        result = cursor.fetchone()

        if result:
            response = result['answer']
        else:
            response = "I don't understand your question."
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
