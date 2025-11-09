#!/usr/bin/python3
import seed

def stream_user_ages():
    """Generator that yields user ages one by one from the database."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    
    for row in cursor:
        yield row['age']
    
    cursor.close()
    connection.close()

def calculate_average_age():
    """Calculate average age using the generator."""
    total_age = 0
    count = 0
    
    for age in stream_user_ages():  # Loop 1
        total_age += age
        count += 1
    
    if count == 0:
        print("No users found.")
        return
    
    average = total_age / count
    print(f"Average age of users: {average:.2f}")

# Run the calculation
if __name__ == "__main__":
    calculate_average_age()