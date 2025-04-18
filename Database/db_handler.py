import sqlite3

def connect_db():
    return sqlite3.connect("agritech.db")

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS farmers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        location TEXT,
        crop TEXT
    )''')
    conn.commit()
    conn.close()

def insert_farmer(name, location, crop):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO farmers (name, location, crop) VALUES (?, ?, ?)", (name, location, crop))
    conn.commit()
    conn.close()
