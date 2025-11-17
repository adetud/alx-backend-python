#!/usr/bin/env python3
"""
Task 1: Reusable Query Context Manager
"""

import sqlite3


class ExecuteQuery:
    """
    Custom context manager that:
    - Opens DB connection
    - Executes a query with parameters
    - Returns results
    """

    def __init__(self, database, query, params=None):
        self.database = database
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        """Open DB connection and execute query"""
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

        if self.params:
            self.cursor.execute(self.query, self.params)
        else:
            self.cursor.execute(self.query)

        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        """Close cursor and DB connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

        # Do not suppress exceptions → return False
        return False


if __name__ == "__main__":
    db_name = "my_database.db"
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery(db_name, query, params) as results:
        for row in results:
            print(row)
