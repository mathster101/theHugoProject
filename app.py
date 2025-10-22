from flask import Flask, render_template, request, jsonify
import os
import random
import sqlite3
from time import sleep, time 
import db_operations.database_operations as db
import db_operations.sqlitedb as sqlitedb

DB_NAME = "mlemdata.db"

def createApp():
    sleep(random.randint(1, 2000) / 999)#just for fun
    sqliteDB = sqlitedb.SQLiteDB(DB_NAME)
    app = Flask(__name__)
    return app, sqliteDB

app, sqliteDB = createApp()
image_folder = os.path.join(app.root_path, 'static', 'images')
image_files = os.listdir(image_folder)

@app.route('/', methods = ["GET"])
def homePage():
    sqliteDB.logVisitTimestamp()
    random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
    image_file = random.choice(image_files)
    visitor_number = sqliteDB.incrementVisitorCountandReturn()
    return render_template('homepage.html', name = random_string, image_file = image_file, visitor_number = visitor_number)

@app.route('/visitorCount', methods = ["GET", "DELETE"])
def visitorCount():
    if request.method == "GET":
        return jsonify({'visitorCount' : sqliteDB.getVisitorCount()}), 200
    if request.method == "DELETE":
        sqliteDB.clearVisitorCount()
        return '', 204

@app.route('/timestamps', methods = ["GET"])
def getAllTimestamps():
    rows = sqliteDB.fetchAllTimestamps()
    return rows

@app.route('/timestamps/top/<count>', methods = ["GET"])
def getTopTimestamps(count = 10):
    rows = getAllTimestamps()
    rows = sorted(rows, key = lambda x : x[1], reverse = True)
    return rows[:int(count)], 200


if __name__ == '__main__':
    app.run(debug=0, host='0.0.0.0')