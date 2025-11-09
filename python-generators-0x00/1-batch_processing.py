#!/usr/bin/python3
"""
Batch processing users from MySQL database using generators
"""

import mysql.connector


def connect_to_prodev():
    """Connect to the ALX_prodev MySQL database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Tendency123.",  # put your MySQL password here if you set one
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows in batches from user_data table
    """
    connection = connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if int(user["age"]) > 25:
                print(user)
