from flask import Flask, render_template, request, jsonify
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

@app.route('/', methods = ["GET"])
def homePage():
    conn = sqlite3.connect(DB_NAME)
    db.logVisitTimestamp(conn)
    random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
    image_file = random.choice(image_files)
    visitor_number = db.incrementVisitorCountandReturn(conn)
    conn.close()
    return render_template('homepage.html', name = random_string, image_file = image_file, visitor_number = visitor_number)

@app.route('/visitorCount', methods = ["GET", "DELETE"])
def visitorCount():
    conn = sqlite3.connect(DB_NAME)
    if request.method == "GET":
        return jsonify({'visitorCount' : db.getVisitorCount(conn)}), 200
    if request.method == "DELETE":
        db.clearVisitorCount(conn)
        return '', 204

@app.route('/timestamps', methods = ["GET"])
def getAllTimestamps():
    conn = sqlite3.connect(DB_NAME)
    rows = db.fetchAllTimestamps(conn)
    return rows

@app.route('/timestamps/top/<count>', methods = ["GET"])
def getTopTimestamps(count = 10):
    rows = getAllTimestamps()
    rows = sorted(rows, key = lambda x : x[1], reverse = True)
    return rows[:int(count)], 200


if __name__ == '__main__':
    app.run(debug=0, host='0.0.0.0')