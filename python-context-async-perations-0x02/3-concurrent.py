#!/usr/bin/env python3
"""
Task 3: Concurrent Asynchronous Database Queries
Uses aiosqlite + asyncio.gather to run queries concurrently
"""

import asyncio
import aiosqlite


async def async_fetch_users(db_name):
    """Fetch all users asynchronously"""
    async with aiosqlite.connect(db_name) as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows


async def async_fetch_older_users(db_name):
    """Fetch users older than 40 asynchronously"""
    async with aiosqlite.connect(db_name) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows


async def fetch_concurrently():
    """Run both queries concurrently using asyncio.gather"""
    db_name = "my_database.db"

    results = await asyncio.gather(
        async_fetch_users(db_name),
        async_fetch_older_users(db_name)
    )

    all_users, older_users = results

    print("All Users:")
    for row in all_users:
        print(row)

    print("\nUsers older than 40:")
    for row in older_users:
        print(row)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())