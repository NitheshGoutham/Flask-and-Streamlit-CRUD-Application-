from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Nith_1104',
        database='records_db'  
    )


def init_db():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Nith_1104'
        )
        
        cursor = connection.cursor()
        
  
        cursor.execute("CREATE DATABASE IF NOT EXISTS records_db;")
        connection.commit()

        
        cursor.execute("USE records_db;")
        
       
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        phone_number VARCHAR(15) NOT NULL,
        role ENUM('Software Engineer', 'Associate Software Engineer', 'Fullstack Developer') NOT NULL,
        experience FLOAT NOT NULL,
        current_ctc FLOAT NOT NULL,
        expected_ctc FLOAT NOT NULL,
        notice_period ENUM('Immediate joiner', 'Less than 15 days','1 month','2 months','3 months') NOT NULL
    );
""")

        connection.commit()
        print("Database initialized!")
    except Error as e:
        print(f"Error initializing database: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route("/records", methods=["GET"])
def get_records():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM records")
        records = cursor.fetchall()
        return jsonify(records)
    except Error as e:
        return jsonify({"error": f"Error fetching records: {e}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route("/record", methods=["POST"])
def add_record():
    data = request.json
    name = data["name"]
    email = data["email"]
    phone_number = data["phone_number"]
    role = data["role"]
    experience = data["experience"]
    current_ctc = data["current_ctc"]
    expected_ctc = data["expected_ctc"]
    notice_period = data["notice_period"]
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO records (name, email, phone_number, role, experience, current_ctc, expected_ctc, notice_period)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, email, phone_number, role, experience, current_ctc, expected_ctc, notice_period))
        connection.commit()
        return jsonify({"message": "Record added!"}), 201
    except Error as e:
        return jsonify({"error": f"Error adding record: {e}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route("/record/<int:record_id>", methods=["PUT"])
def update_record(record_id):
    data = request.json
    name = data["name"]
    email = data["email"]
    phone_number = data["phone_number"]
    role = data["role"]
    experience = data["experience"]
    current_ctc = data["current_ctc"]
    expected_ctc = data["expected_ctc"]
    notice_period = data["notice_period"]
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE records SET name=%s, email=%s, phone_number=%s, role=%s, experience=%s, current_ctc=%s, expected_ctc=%s, notice_period=%s
            WHERE id=%s
        """, (name, email, phone_number, role, experience, current_ctc, expected_ctc, notice_period, record_id))
        connection.commit()
        return jsonify({"message": "Record updated!"})
    except Error as e:
        return jsonify({"error": f"Error updating record: {e}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route("/record/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM records WHERE id=%s", (record_id,))
        connection.commit()
        return jsonify({"message": "Record deleted!"})
    except Error as e:
        return jsonify({"error": f"Error deleting record: {e}"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    init_db()  
    app.run(port=5000)
