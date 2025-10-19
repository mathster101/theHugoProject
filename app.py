from flask import Flask, render_template
import os
import random
import sqlite3
from time import sleep, time 
import db_operations.database_operations as db
DB_NAME = "mlemdata.db"

def createApp():
    sleep(random.randint(1, 2000) / 999)#just for fun
    conn = sqlite3.connect(DB_NAME)
    db.initialize(conn)
    conn.close()
    app = Flask(__name__)
    return app

app = createApp()
image_folder = os.path.join(app.root_path, 'static', 'images')
image_files = os.listdir(image_folder)

@app.route('/')
def homePage():
    conn = sqlite3.connect(DB_NAME)
    db.logVisitTimestamp(conn)
    random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
    image_file = random.choice(image_files)
    visitor_number = db.incrementVisitorCountandReturn(conn)
    conn.close()
    return render_template('homepage.html', name = random_string, image_file = image_file, visitor_number = visitor_number)

@app.route('/timestamps')
def getAllTimestamps():
    conn = sqlite3.connect(DB_NAME)
    rows = db.fetchAllTimestamps(conn)
    return rows


if __name__ == '__main__':
    app.run(debug=0, host='0.0.0.0')