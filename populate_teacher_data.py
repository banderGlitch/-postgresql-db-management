"""
Script to automatically populate teacher table with sample data
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

# Sample teacher data
teachers = [
    ('Dr. John Smith', 'john.smith@coep.ac.in', 'Computer Science', '9876543210'),
    ('Prof. Sarah Johnson', 'sarah.johnson@coep.ac.in', 'Mathematics', '9876543211'),
    ('Dr. Michael Brown', 'michael.brown@coep.ac.in', 'Physics', '9876543212'),
    ('Prof. Emily Davis', 'emily.davis@coep.ac.in', 'Chemistry', '9876543213'),
    ('Dr. Robert Wilson', 'robert.wilson@coep.ac.in', 'Electronics', '9876543214')
]

# Insert teachers
inserted_count = 0
for teacher in teachers:
    try:
        cur.execute("""
            INSERT INTO teacher (name, email, department, phone)
            VALUES (%s, %s, %s, %s)
        """, teacher)
        inserted_count += 1
    except psycopg2.IntegrityError:
        print(f"⚠ Teacher {teacher[0]} already exists, skipping...")
        conn.rollback()
        continue

# Commit the changes
conn.commit()
print(f"✓ {inserted_count} teachers inserted successfully!")

# Display all teachers
cur.execute("SELECT id, name, email, department FROM teacher")
rows = cur.fetchall()
print("\nAll Teachers:")
print("-" * 80)
for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Department: {row[3]}")

# Close the connection
cur.close()
conn.close()

