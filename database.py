import sqlite3

connection = sqlite3.connect("database.db")

cursor = connection.cursor()


# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL,

    email TEXT NOT NULL UNIQUE,

    password TEXT NOT NULL

)
""")


# Tasks table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    title TEXT NOT NULL,

    description TEXT,

    status TEXT DEFAULT 'Pending',

     due_date DATETIME,

    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE

)
""")

try:
    cursor.execute("""
        ALTER TABLE tasks
        ADD COLUMN due_date DATETIME
    """)
    print("due_date column added.")
except sqlite3.OperationalError:
    print("due_date column already exists.")


connection.commit()

connection.close()


print("Database setup completed")
