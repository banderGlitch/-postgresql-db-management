"""
PostgreSQL Python Example - Student Management with Image Storage
"""

import psycopg2  # pyright: ignore[reportMissingModuleSource]
import os
from dotenv import load_dotenv
from urllib.request import urlopen

# Load environment variables
load_dotenv()

# Connect to the database
conn = psycopg2.connect(
    dbname=os.getenv('POSTGRES_DB', 'COEP'),
    user=os.getenv('POSTGRES_USER', 'postgres'),
    password=os.getenv('POSTGRES_PASSWORD', ''),
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=os.getenv('POSTGRES_PORT', '5432')
)

# Create a cursor object
cur = conn.cursor()

# Take input from user
name = input("Enter student name: ")
mis_number = input("Enter MIS number: ")
age = int(input("Enter age: "))
city = input("Enter city: ")
image_path = input("Enter image path: ")

# Check if MIS number already exists
cur.execute("SELECT mis_number FROM student WHERE mis_number = %s", (mis_number,))
if cur.fetchone():
    print("MIS number already exists.")
else:
    # Read the image file and convert it to bytes
    if image_path.startswith('http://') or image_path.startswith('https://'):
        # Download image from URL
        with urlopen(image_path) as response:
            image_bytes = response.read()
    else:
        # Read from local file
        with open(image_path, 'rb') as image_file:
            image_bytes = image_file.read()
    
    # Insert data into the student table
    cur.execute("""
        INSERT INTO student (name, mis_number, age, city, image_path, image_data)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, mis_number, age, city, image_path, psycopg2.Binary(image_bytes)))
    
    # Commit the changes
    conn.commit()
    print("Student inserted successfully!")

# Fetch all students from the database
cur.execute("SELECT * FROM student")
rows = cur.fetchall()
for row in rows:
    print(row)

# Close the connection
cur.close()
conn.close()
