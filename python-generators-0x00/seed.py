#!/usr/bin/env python3
"""
seed.py
Utilities to create/connect to MySQL DB, create table, insert CSV data,
and stream rows using Python generators for memory-efficient processing.
"""

import csv
import uuid
import mysql.connector
from mysql.connector import errorcode

# ======== CONFIG: adapt these to your local environment ========
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "Tendency123."
DB_NAME = "ALX_prodev"
# =============================================================

def connect_db():
    """
    Connect to MySQL server (NOT to a specific database).
    Returns a mysql.connector connection object or None on failure.
    """
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            autocommit=True  # helpful for immediate CREATE DATABASE
        )
        return conn
    except mysql.connector.Error as err:
        print(f"[connect_db] Error: {err}")
        return None

def create_database(connection):
    """
    Create the ALX_prodev database if it does not exist.
    Uses the provided server-level connection (not db-specific).
    """
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        print(f"Database {DB_NAME} ensured present.")
    except mysql.connector.Error as err:
        print(f"[create_database] Error: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    """
    Connect to the ALX_prodev database and return the connection.
    """
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            autocommit=False  # we'll commit manually after inserts
        )
        return conn
    except mysql.connector.Error as err:
        print(f"[connect_to_prodev] Error: {err}")
        return None

def create_table(connection):
    """
    Create user_data table if it doesn't exist.
    user_id is stored as CHAR(36) to hold a UUID string (xxxxxxxx-xxxx-...).
    """
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) NOT NULL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age INT NOT NULL,
        INDEX idx_email (email)
    ) ENGINE=InnoDB;
    """
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_sql)
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"[create_table] Error: {err}")
    finally:
        cursor.close()

def insert_data(connection, csv_path):
    """
    Insert data from csv_path into user_data table.
    - If a row in CSV contains a 'user_id' column, we use it. Otherwise we generate UUID.
    - Uses "INSERT IGNORE" style logic by checking for existing email to avoid duplicates.
    """
    cursor = connection.cursor()

    # read CSV
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows_inserted = 0
        for row in reader:
            # normalize keys (handle CSV that might have headers in various case)
            # Expected headers: user_id (optional), name, email, age
            user_id = row.get('user_id') or row.get('id') or None
            name = row.get('name') or row.get('Name') or None
            email = row.get('email') or row.get('Email') or None
            age = row.get('age') or row.get('Age') or None

            if not (name and email and age):
                # skip invalid row, but you could also raise/notify
                print(f"[insert_data] Skipping invalid CSV row: {row}")
                continue

            if not user_id:
                user_id = str(uuid.uuid4())

            # ensure age is an integer
            try:
                age_val = int(float(age))
            except Exception:
                # fallback: skip or set default age
                print(f"[insert_data] invalid age '{age}' for {email}, skipping.")
                continue

            # Option 1: Use INSERT ... ON DUPLICATE KEY UPDATE if you have a unique key on email.
            # We didn't declare email UNIQUE, so we first check existence by email.
            cursor.execute("SELECT user_id FROM user_data WHERE email = %s LIMIT 1;", (email,))
            existing = cursor.fetchone()
            if existing:
                # skip duplicates by email
                # If you want to update, use UPDATE here
                continue

            # Insert
            try:
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s);",
                    (user_id, name, email, age_val)
                )
                rows_inserted += 1
            except mysql.connector.Error as err:
                print(f"[insert_data] Insert error for {email}: {err}")
                # continue on error

        connection.commit()
    cursor.close()
    print(f"Inserted {rows_inserted} new rows from {csv_path}")

# ------------------ Generators for streaming rows ------------------

def stream_user_data_one_by_one(connection):
    """
    Generator that streams rows from user_data one-by-one.
    Uses a server-side cursor (unbuffered) to avoid loading all rows into memory.

    Usage:
        for row in stream_user_data_one_by_one(conn):
            process(row)
    """
    # create a server-side (unbuffered) cursor
    cursor = connection.cursor(buffered=False)
    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data;")
        # fetchone in a loop to yield row-by-row
        row = cursor.fetchone()
        while row:
            yield row
            row = cursor.fetchone()
    finally:
        cursor.close()

def stream_user_data_in_batches(connection, batch_size=1000):
    """
    Generator that yields lists of rows (batches), each batch up to batch_size.
    Good for processing large tables in chunks.
    """
    cursor = connection.cursor(buffered=False)
    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data;")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
    finally:
        cursor.close()

# ------------------ Optional convenience main for local test ------------------

if __name__ == "__main__":
    # quick test workflow (local use)
    conn = connect_db()
    if not conn:
        raise SystemExit("Cannot connect to MySQL server. Fix DB credentials or server.")
    create_database(conn)
    conn.close()

    conn = connect_to_prodev()
    if not conn:
        raise SystemExit("Cannot connect to ALX_prodev database.")
    create_table(conn)

    # If you have user_data.csv in current dir, insert it:
    import os
    csv_file = "user_data.csv"
    if os.path.exists(csv_file):
        insert_data(conn, csv_file)
        # print a few rows
        c = conn.cursor()
        c.execute("SELECT * FROM user_data LIMIT 5;")
        print(c.fetchall())
        c.close()
    else:
        print(f"No {csv_file} found in current directory. Skipping insert_data step.")

    # show generator usage
    print("Streaming first 3 rows using generator:")
    count = 0
    for r in stream_user_data_one_by_one(conn):
        print(r)
        count += 1
        if count >= 3:
            break

    conn.close()