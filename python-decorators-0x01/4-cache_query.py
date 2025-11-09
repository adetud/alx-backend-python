import time
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

# Task 4 decorator: cache query results
query_cache = {}  # global cache dictionary

def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[1] if len(args) > 1 else None)
        if query in query_cache:
            print("[LOG] Using cached result.")
            return query_cache[query]
        result = func(*args, **kwargs)
        query_cache[query] = result
        print("[LOG] Query result cached.")
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call → fetches from DB and caches
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call → uses cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
