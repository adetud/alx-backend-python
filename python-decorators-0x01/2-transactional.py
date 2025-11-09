import sqlite3
import functools

# Task 1 decorator: handle DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Task 2 decorator: handle transactions
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # commit if no exception
            print("[LOG] Transaction committed successfully.")
            return result
        except Exception as e:
            conn.rollback()  # rollback on error
            print(f"[ERROR] Transaction rolled back due to: {e}")
            raise  # re-raise the exception
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )

# Test updating user email
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
print("[LOG] User email update finished.")
