from flask import Flask, render_template
import os
import random
import sqlite3
from time import sleep, time 

DB_NAME = "mlemdata.db"


def initializeCounterTable(conn: sqlite3.Connection):
    try:
        cursor = conn.cursor()
        cursor.execute("""SELECT name FROM sqlite_master
                    WHERE type='table' AND name='counter'""")
        if cursor.fetchone() == None:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS counter (
                id INTEGER PRIMARY KEY,
                count INTEGER
            )
            """)
            cursor.execute("INSERT INTO counter VALUES (0,0 )")
            conn.commit()
            print("table \'counter\' created")
        else:
            print("db already initialized!")
    except:
        print("counter db already initialized")

def initializeTimestampTable(conn: sqlite3.Connection):
    try:
        cursor = conn.cursor()
        # Create the table if it doesn't already exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS timestamp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unix_time INTEGER UNIQUE,
            count INTEGER NOT NULL
        )
        ''')
        conn.commit()
    except:
        print("timestamp db already initialized")

def incrementVisitorCountandReturn(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM counter WHERE id = 0")
    current_val = cursor.fetchone()
    cursor.execute("""UPDATE counter 
                   SET count = ?
                   WHERE id = 0""",
                   ((current_val[1] + 1 ),))
    conn.commit()
    return current_val[1] + 1

def fetchAllTimestamps(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT unix_time, count FROM timestamp")
    result = cursor.fetchall()
    return result
    


def logVisitTimestamp(conn: sqlite3.Connection):
    cursor = conn.cursor()
    unix_time = int(time())
    cursor.execute("""
        INSERT INTO timestamp (unix_time, count)
        VALUES (?, 1)
        ON CONFLICT(unix_time) DO UPDATE SET count = count + 1
    """, (unix_time,))
    conn.commit()


def createApp():
    sleep(random.randint(1, 2000) / 999)#just for fun
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA journal_mode=WAL;")
    initializeTimestampTable(conn)
    initializeCounterTable(conn)
    conn.close()
    app = Flask(__name__)
    return app

app = createApp()
image_folder = os.path.join(app.root_path, 'static', 'images')
image_files = os.listdir(image_folder)

@app.route('/')
def homePage():
    conn = sqlite3.connect(DB_NAME)
    logVisitTimestamp(conn)
    random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
    image_file = random.choice(image_files)
    visitor_number = incrementVisitorCountandReturn(conn)
    conn.close()
    return render_template('homepage.html', name = random_string, image_file = image_file, visitor_number = visitor_number)

@app.route('/timestamps')
def getAllTimestamps():
    conn = sqlite3.connect(DB_NAME)
    rows = fetchAllTimestamps(conn)
    return rows


if __name__ == '__main__':
    app.run(debug=0, host='0.0.0.0')