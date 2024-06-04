from flask import Flask, json, request, jsonify, render_template
import sqlite3
from datetime import datetime
import random
import time
import threading

app = Flask(__name__)

def db_connection():
    conn = sqlite3.connect('AIoT_practice.sqlite')
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

def create_table():
    conn = db_connection()
    curs = conn.cursor()
    curs.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    temperature REAL,
                    humidity REAL,
                    timestamp TEXT)''')
    conn.commit()
    conn.close()

@app.route('/add_data', methods=['POST'])
def add_data():
        req = json.loads(request.data.decode('utf-8'))
        conn =db_connection()
        cursor = conn.cursor()
        timestamp = datetime.now()
        cursor.execute('''
            INSERT INTO sensor_data (temperature, humidity, timestamp)
            VALUES (?, ?, ?)
        ''', (req['temperature'], req['humidity'],timestamp))
        conn.commit()
        conn.close()

        return 'Success', 200


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/realtime')
def realtime():
    return render_template('realtime.html')

@app.route('/range')
def range():
    return render_template('specifiedtimeofdata.html')

@app.route('/data/realtime', methods=['GET'])
def get_realtime_data():
    conn = db_connection()
    curs = conn.cursor()
    curs.execute("SELECT temperature, humidity, timestamp FROM sensor_data ORDER BY timestamp DESC LIMIT 1")
    data = curs.fetchone()
    conn.close()
    return jsonify({'temperature': data['temperature'], 'humidity': data['humidity'], 'timestamp': data['timestamp']})

@app.route('/data/range', methods=['GET'])
def get_data_range():
    start = request.args.get('start')
    end = request.args.get('end')
    conn = db_connection()
    curs = conn.cursor()
    curs.execute("SELECT * FROM sensor_data WHERE timestamp BETWEEN ? AND ?", (start, end))
    data = curs.fetchall()
    conn.close()
    return jsonify([{"temperature": row['temperature'], "humidity": row['humidity'], "timestamp": row['timestamp']} for row in data])

if __name__ == '__main__':
    create_table()
    app.run(debug=True, host='0.0.0.0', port=5000)
