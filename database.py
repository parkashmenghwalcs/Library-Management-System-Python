import sqlite3

def create_database():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        year INTEGER
    )
    """)

    conn.commit()
    conn.close()

create_database()