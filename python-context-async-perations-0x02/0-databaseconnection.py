#!/usr/bin/env python3
"""
0-databaseconnection.py
Custom class-based context manager for SQLite database connections.
"""

import sqlite3


class DatabaseConnection:
    """A class-based context manager for database connections."""

    def __init__(self, db_name):
        """Initialize with database filename."""
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        """Open the database connection."""
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the connection when exiting the context."""
        if self.connection:
            self.connection.close()


# Example usage
if __name__ == "__main__":
    db_file = "my_database.db"  # Use your SQLite database file here

    # Using the custom context manager
    with DatabaseConnection(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()

        # Print results
        for row in results:
            print(row)