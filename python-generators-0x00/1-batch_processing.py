#!/usr/bin/python3
"""
Batch processing users from CSV using generators
"""

import csv


def stream_users_in_batches(batch_size):
    """
    Generator that reads the CSV file and yields users in batches
    of size 'batch_size'
    """
    batch = []
    with open("user_data.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []
        # yield the remaining rows if any
        if batch:
            yield batch


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25
    and prints them
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if int(user['age']) > 25:
                print(user)