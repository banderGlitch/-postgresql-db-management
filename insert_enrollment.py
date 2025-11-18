"""
Script to insert enrollment data into the database
"""

import psycopg2  # pyright: ignore[reportMissingModuleSource]
import os
from dotenv import load_dotenv
from datetime import datetime

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
student_id = int(input("Enter student ID: "))
course_id = int(input("Enter course ID: "))
enrollment_date = input("Enter enrollment date (YYYY-MM-DD) or press Enter for today: ")
grade = input("Enter grade (optional, press Enter to skip): ")
status = input("Enter status (enrolled/completed/dropped, default: enrolled): ")

# Check if student exists
cur.execute("SELECT id, name FROM student WHERE id = %s", (student_id,))
student = cur.fetchone()
if not student:
    print(f"✗ Error: Student with ID {student_id} does not exist!")
    cur.close()
    conn.close()
    exit()

print(f"Student found: {student[1]}")

# Check if course exists
cur.execute("SELECT id, course_code, course_name FROM course WHERE id = %s", (course_id,))
course = cur.fetchone()
if not course:
    print(f"✗ Error: Course with ID {course_id} does not exist!")
    cur.close()
    conn.close()
    exit()

print(f"Course found: {course[1]} - {course[2]}")

# Use today's date if not provided
if not enrollment_date:
    enrollment_date = datetime.now().strftime('%Y-%m-%d')

# Use default status if not provided
if not status:
    status = 'enrolled'

# Insert data into the enrollment table
try:
    cur.execute("""
        INSERT INTO enrollment (student_id, course_id, enrollment_date, grade, status)
        VALUES (%s, %s, %s, %s, %s)
    """, (student_id, course_id, enrollment_date, grade if grade else None, status))
    
    # Commit the changes
    conn.commit()
    print(f"✓ Enrollment created successfully!")
except psycopg2.IntegrityError:
    print("✗ Error: Student is already enrolled in this course!")
    conn.rollback()

# Close the connection
cur.close()
conn.close()

