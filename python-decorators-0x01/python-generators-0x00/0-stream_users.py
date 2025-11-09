#!/usr/bin/python3
"""
Generator that streams rows from the user_data table
one by one using yield.
"""

import csv


def stream_users():
    """Generator that yields one user at a time from user_data.csv"""
    with open("user_data.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row