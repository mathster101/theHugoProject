import sqlite3


conn = sqlite3.connect("test.db")

cursor = conn.cursor()
# Create a simple table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
)''')
#cursor.execute("INSERT INTO users (name, age) VALUES (?,?)", ("hugo", 3))
#conn.commit()

cursor.execute("select name, age from users")
print(cursor.fetchall())
conn.close()
print(f"row inserted successfully")