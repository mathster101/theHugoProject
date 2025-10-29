from flask import Flask, render_template, request, jsonify
import os
import random
import sqlite3
from time import sleep
import db_operations.sqlitedb as sqlitedb
import db_operations.redisdb as redisdb

#DB_TYPE = "SQLite"
DB_TYPE = "Redis"
DB_NAME_SQLite = "mlemdata.db"



def createApp():
    sleep(random.randint(1, 2000) / 999)
    if DB_TYPE ==  "SQLite":
        database = sqlitedb.SQLiteDB(DB_NAME_SQLite)
    elif DB_TYPE == "Redis":
        database = redisdb.RedisDB()
    else:
        database = None
    app = Flask(__name__)
    return app, database

app, database = createApp()
image_folder = os.path.join(app.root_path, 'static', 'images')
image_files = os.listdir(image_folder)

@app.route('/', methods = ["GET"])
def homePage():
    database.logVisitTimestamp()
    random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
    image_file = random.choice(image_files)
    visitor_number = database.incrementVisitorCountandReturn()
    return render_template('homepage.html', name = random_string, image_file = image_file, visitor_number = visitor_number)

@app.route('/visitorCount', methods = ["GET", "DELETE"])
def visitorCount():
    if request.method == "GET":
        return jsonify({'visitorCount' : database.getVisitorCount()}), 200
    if request.method == "DELETE":
        database.clearVisitorCount()
        return '', 204

@app.route('/timestamps', methods = ["GET"])
def getAllTimestamps():
    rows = database.fetchAllTimestamps()
    return rows

@app.route('/timestamps/top/<count>', methods = ["GET"])
def getTopTimestamps(count = 10):
    rows = getAllTimestamps()
    rows = sorted(rows, key = lambda x : x[1], reverse = True)
    return rows[:int(count)], 200


if __name__ == '__main__':
    app.run(debug=1, host='0.0.0.0')