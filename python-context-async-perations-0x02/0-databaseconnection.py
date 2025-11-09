import sqlite3
import os

class DatabaseConnection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def __enter__(self):
        print("Opening database connection...")
        self.conn = sqlite3.connect(self.db_file)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            print("Closing database connection...")
            self.conn.close()


if __name__ == "__main__":
    db_file = "test.db"

    # Check if database exists; if not, create table and sample data
    if not os.path.exists(db_file):
        print("Database does not exist. Creating database and table...")
        with DatabaseConnection(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            """)
            cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Alice", "alice@example.com"))
            cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Bob", "bob@example.com"))
            conn.commit()
            print("Table and sample data created.")

    # Now fetch the data
    print("Fetching users from the database...")
    with DatabaseConnection(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        if rows:
            print("Rows found:")
            for row in rows:
                print(row)
        else:
            print("No rows found in the users table.")
