import sqlite3
from time import time


def initialize(conn: sqlite3.Connection):
    conn.execute("PRAGMA journal_mode=WAL;")
    initializeTimestampTable(conn)
    initializeCounterTable(conn)

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

def getVisitorCount(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT count FROM counter where id = 0")
    current_val = cursor.fetchone()
    return int(current_val[0])

def clearVisitorCount(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("UPDATE counter SET count = ? WHERE id = 0", (0,))
    conn.commit()

def incrementVisitorCountandReturn(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE counter
        SET count = count + 1
        WHERE id = 0
    """)
    conn.commit()
    cursor.execute("SELECT count FROM counter WHERE id = 0")
    return cursor.fetchone()[0]


def logVisitTimestamp(conn: sqlite3.Connection):
    cursor = conn.cursor()
    unix_time = int(time())
    cursor.execute("""
        INSERT INTO timestamp (unix_time, count)
        VALUES (?, 1)
        ON CONFLICT(unix_time) DO UPDATE SET count = count + 1
    """, (unix_time,))
    conn.commit()

def fetchAllTimestamps(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT unix_time, count FROM timestamp")
    result = cursor.fetchall()
    return result