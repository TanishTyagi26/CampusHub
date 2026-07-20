import sqlite3

connection = sqlite3.connect("database/campushub.db")
cursor = connection.cursor()

# ==========================
# Students Table
# ==========================
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

# ==========================
# Faculty Table
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS faculty(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    department TEXT NOT NULL
)
""")

# ==========================
# Admin Table
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# ==========================
# Notes Table
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS notes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    subject TEXT NOT NULL,
    filename TEXT NOT NULL
)
""")

# Add uploaded_by column if it doesn't exist
try:
    cursor.execute("""
    ALTER TABLE notes
    ADD COLUMN uploaded_by TEXT DEFAULT 'Student'
    """)
except:
    pass

# ==========================
# Announcements Table
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS announcements(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL
)
""")

# ==========================
# Default Admin Account
# ==========================
cursor.execute("""
INSERT OR IGNORE INTO admin(username, password)
VALUES('admin', 'admin123')
""")

connection.commit()
connection.close()

print("Database created successfully!")