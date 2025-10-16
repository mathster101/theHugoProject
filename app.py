from flask import Flask, render_template
import os
import random
import sqlite3


def initializeTable(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("""select name from sqlite_master
                   where type='table' and name='counter'""")
    
    if cursor.fetchone() == None:
        cursor.execute("""
            CREATE TABLE counter (
                id INTEGER PRIMARY KEY,
                count INTEGER
            )
        """)
        cursor.execute("insert into counter values (0,0 )")
        conn.commit()
        print("table \'counter\' created")
    else:
        print("db already initialized!")

def incrementCountandReturn(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("select * from counter where id = 0")
    current_val = cursor.fetchone()
    cursor.execute("""update counter 
                   set count = ?
                   where id = 0""",
                   ((current_val[1] + 1 ),))
    conn.commit()
    return current_val[1] + 1

app = Flask(__name__)

conn = sqlite3.connect("mlemdata.db")
initializeTable(conn)
conn.close()

image_folder = os.path.join(app.root_path, 'static', 'images')
image_files = os.listdir(image_folder)

@app.route('/')
def home():
    conn = sqlite3.connect("mlemdata.db")
    random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
    image_file = random.choice(image_files)
    visitor_number = incrementCountandReturn(conn)
    conn.close()
    return render_template('homepage.html', name = random_string, image_file = image_file, visitor_number = visitor_number)

if __name__ == '__main__':
    app.run(debug=0, host='0.0.0.0')