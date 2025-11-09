#!/usr/bin/python3
from itertools import islice

# Import the generator modules
stream_users_module = __import__('0-stream_users')
batch_module = __import__('1-batch_processing')
lazy_module = __import__('2-lazy_paginate')

print("===== STREAMING SINGLE ROWS =====")
# Stream first 5 users one by one
for user in islice(stream_users_module.stream_users(), 5):
    print(user)

print("\n===== BATCH PROCESSING (Users > 25) =====")
# Process in batches of 50
batch_module.batch_processing(50)

print("\n===== LAZY PAGINATION (Pages of 100) =====")
# Lazy pagination
for page in lazy_module.lazy_pagination(100):
    for user in page[:5]:  # show only first 5 users per page for demo
        print(user)
    break  # Remove break if you want to show all pages