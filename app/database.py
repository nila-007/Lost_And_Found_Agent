import sqlite3

DB_NAME = "lostiq.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lost_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        category TEXT,
        description TEXT,
        location TEXT,
        lost_date_time TEXT,
        status TEXT DEFAULT 'lost'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS found_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        category TEXT,
        description TEXT,
        location TEXT,
        found_date_time TEXT,
        status TEXT DEFAULT 'found'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS investigation_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    description TEXT,
    lost_location TEXT,
    lost_date_time TEXT,
    status TEXT DEFAULT 'searching',
    current_step TEXT,
    possible_matches TEXT,
    last_updated TEXT
    )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()
    print("LOSTIQ database and tables are ready!")