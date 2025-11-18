"""
Script to automatically populate student table with sample data
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

# Sample student data
students = [
    ('Rajesh Kumar', 'MIS2024001', 20, 'Pune', None, None),
    ('Priya Sharma', 'MIS2024002', 19, 'Mumbai', None, None),
    ('Amit Patel', 'MIS2024003', 21, 'Ahmedabad', None, None),
    ('Sneha Desai', 'MIS2024004', 20, 'Surat', None, None),
    ('Vikram Singh', 'MIS2024005', 22, 'Delhi', None, None),
    ('Anjali Mehta', 'MIS2024006', 19, 'Bangalore', None, None),
    ('Rahul Joshi', 'MIS2024007', 21, 'Nagpur', None, None),
    ('Kavita Reddy', 'MIS2024008', 20, 'Hyderabad', None, None)
]

# Insert students
inserted_count = 0
for student in students:
    try:
        cur.execute("""
            INSERT INTO student (name, mis_number, age, city, image_path, image_data)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, student)
        inserted_count += 1
    except psycopg2.IntegrityError:
        print(f"⚠ Student {student[0]} (MIS: {student[1]}) already exists, skipping...")
        conn.rollback()
        continue

# Commit the changes
conn.commit()
print(f"✓ {inserted_count} students inserted successfully!")

# Display all students
cur.execute("SELECT id, name, mis_number, age, city FROM student ORDER BY id")
rows = cur.fetchall()
print("\nAll Students:")
print("-" * 80)
for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, MIS: {row[2]}, Age: {row[3]}, City: {row[4]}")

# Close the connection
cur.close()
conn.close()

