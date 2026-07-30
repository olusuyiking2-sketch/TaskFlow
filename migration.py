import sqlite3

connection = sqlite3.connect("database.db")

connection.execute("""
ALTER TABLE tasks ADD COLUMN due_date DATETIME;
""")

connection.commit()

connection.close()

print("Database migration completed")