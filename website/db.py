import sqlite3

conn = sqlite3.connect('Outputdb.db')
print("Opened database successfully")

conn.execute('CREATE TABLE students (username TEXT, image TEXT, BrainTumor text, details TEXT)')
print("Table created successfully")
conn.close()