import sqlite3

# Connect to the DB
connection = sqlite3.connect('database.db')

# Open the schema.sql with the format and apply it to the DB
with open('schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()
