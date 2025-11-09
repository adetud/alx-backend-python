import sqlite3
import functools

# Decorator to handle database connection automatically
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # open DB connection
        try:
            return func(conn, *args, **kwargs)  # pass connection to the function
        finally:
            conn.close()  # ensure connection is closed
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Test fetching user by ID
user = get_user_by_id(user_id=1)
print(user)
