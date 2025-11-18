"""
Script to automatically populate course table with sample data
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

# Get teacher IDs first
cur.execute("SELECT id, name FROM teacher ORDER BY id")
teachers = cur.fetchall()

if not teachers:
    print("✗ Error: No teachers found! Please run populate_teacher_data.py first.")
    cur.close()
    conn.close()
    exit()

# Sample course data (using first 5 teachers)
courses = [
    ('CS101', 'Introduction to Programming', teachers[0][0], 3, 'Basic programming concepts'),
    ('CS201', 'Data Structures', teachers[0][0], 4, 'Arrays, linked lists, trees'),
    ('MATH101', 'Calculus I', teachers[1][0], 3, 'Differential and integral calculus'),
    ('MATH201', 'Linear Algebra', teachers[1][0], 4, 'Vectors, matrices, systems of equations'),
    ('PHY101', 'Mechanics', teachers[2][0], 3, 'Classical mechanics and dynamics'),
    ('CHEM101', 'Organic Chemistry', teachers[3][0], 3, 'Introduction to organic compounds'),
    ('ECE101', 'Digital Electronics', teachers[4][0], 4, 'Logic gates and digital circuits')
]

# Insert courses
inserted_count = 0
for course in courses:
    try:
        cur.execute("""
            INSERT INTO course (course_code, course_name, teacher_id, credits, description)
            VALUES (%s, %s, %s, %s, %s)
        """, course)
        inserted_count += 1
    except psycopg2.IntegrityError:
        print(f"⚠ Course {course[0]} already exists, skipping...")
        conn.rollback()
        continue

# Commit the changes
conn.commit()
print(f"✓ {inserted_count} courses inserted successfully!")

# Display all courses with teacher names
cur.execute("""
    SELECT c.id, c.course_code, c.course_name, c.credits, t.name AS teacher_name
    FROM course c
    JOIN teacher t ON c.teacher_id = t.id
    ORDER BY c.id
""")
rows = cur.fetchall()
print("\nAll Courses:")
print("-" * 80)
for row in rows:
    print(f"ID: {row[0]}, Code: {row[1]}, Name: {row[2]}, Credits: {row[3]}, Teacher: {row[4]}")

# Close the connection
cur.close()
conn.close()

