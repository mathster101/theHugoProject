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


def incrementCount(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("select * from counter where id = 0")
    current_val = cursor.fetchone()
    cursor.execute("""update counter 
                   set count = ?
                   where id = 0""",
                   ((current_val[1] + 1 ),))
    conn.commit()
    print(current_val)
    return


conn = sqlite3.connect("test2.db")
initializeTable(conn)
incrementCount(conn)
conn.close()
