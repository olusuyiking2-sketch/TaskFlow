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

    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE

)
""")


connection.commit()

connection.close()


print("Database setup completed")
