import sqlite3

connection = sqlite3.connect("database/campushub.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    branch TEXT NOT NULL,
    year TEXT NOT NULL
)
""")

connection.commit()
connection.close()

print("Database created successfully!")