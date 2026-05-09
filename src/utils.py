import sqlite3

DB_PATH = "db/market.db"

def create_database():
    connection = sqlite3.connect(DB_PATH)

    with open("db/schema.sql", "r") as file:
        connection.executescript(file.read())

    connection.commit()
    connection.close()

    print("Database created successfully.")