"""
Script to insert course data into the database
"""

import psycopg2  # pyright: ignore[reportMissingModuleSource]
import os
from dotenv import load_dotenv

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

cur = conn.cursor()

# Take input from user
course_code = input("Enter course code: ")
course_name = input("Enter course name: ")
teacher_id = int(input("Enter teacher ID: "))
credits = int(input("Enter credits: "))
description = input("Enter description (optional, press Enter to skip): ")

# Check if teacher exists
cur.execute("SELECT id, name FROM teacher WHERE id = %s", (teacher_id,))
teacher = cur.fetchone()
if not teacher:
    print(f"✗ Error: Teacher with ID {teacher_id} does not exist!")
    cur.close()
    conn.close()
    exit()

print(f"Teacher found: {teacher[1]}")

# Insert data into the course table
try:
    cur.execute("""
        INSERT INTO course (course_code, course_name, teacher_id, credits, description)
        VALUES (%s, %s, %s, %s, %s)
    """, (course_code, course_name, teacher_id, credits, description if description else None))
    
    # Commit the changes
    conn.commit()
    print(f"✓ Course {course_code} inserted successfully!")
except psycopg2.IntegrityError:
    print("✗ Error: Course code already exists!")
    conn.rollback()

# Close the connection
cur.close()
conn.close()

