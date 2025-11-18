"""
Script to automatically populate enrollment table with sample data
"""

import psycopg2  # pyright: ignore[reportMissingModuleSource]
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

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

# Get student IDs
cur.execute("SELECT id, name FROM student ORDER BY id LIMIT 5")
students = cur.fetchall()

if not students:
    print("✗ Error: No students found! Please add some students first using postgresDB.py")
    cur.close()
    conn.close()
    exit()

# Get course IDs
cur.execute("SELECT id, course_code FROM course ORDER BY id")
courses = cur.fetchall()

if not courses:
    print("✗ Error: No courses found! Please run populate_course_data.py first.")
    cur.close()
    conn.close()
    exit()

# Sample enrollment data
enrollments = []
base_date = datetime.now() - timedelta(days=30)

# Enroll each student in 2-3 courses
for i, student in enumerate(students):
    student_id = student[0]
    # Enroll in first 2-3 courses
    num_courses = min(3, len(courses))
    for j in range(num_courses):
        course_id = courses[j][0]
        enrollment_date = (base_date + timedelta(days=i*2 + j)).strftime('%Y-%m-%d')
        
        # Assign grades for some enrollments
        if j == 0:  # First course gets a grade
            grade = ['A', 'B+', 'A-', 'B', 'A+'][i % 5]
            status = 'completed'
        else:
            grade = None
            status = 'enrolled'
        
        enrollments.append((student_id, course_id, enrollment_date, grade, status))

# Insert enrollments
inserted_count = 0
for enrollment in enrollments:
    try:
        cur.execute("""
            INSERT INTO enrollment (student_id, course_id, enrollment_date, grade, status)
            VALUES (%s, %s, %s, %s, %s)
        """, enrollment)
        inserted_count += 1
    except psycopg2.IntegrityError:
        print(f"⚠ Enrollment already exists, skipping...")
        conn.rollback()
        continue

# Commit the changes
conn.commit()
print(f"✓ {inserted_count} enrollments inserted successfully!")

# Display all enrollments
cur.execute("""
    SELECT 
        s.name AS student_name,
        c.course_code,
        c.course_name,
        e.enrollment_date,
        e.grade,
        e.status
    FROM enrollment e
    JOIN student s ON e.student_id = s.id
    JOIN course c ON e.course_id = c.id
    ORDER BY s.name, c.course_code
""")
rows = cur.fetchall()
print("\nAll Enrollments:")
print("-" * 100)
for row in rows:
    grade_str = f", Grade: {row[4]}" if row[4] else ""
    print(f"Student: {row[0]} | Course: {row[1]} - {row[2]} | Date: {row[3]}{grade_str} | Status: {row[5]}")

# Close the connection
cur.close()
conn.close()

