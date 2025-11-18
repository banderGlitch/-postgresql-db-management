"""
Examples of different JOIN operations
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

print("="*100)
print("JOIN EXAMPLES")
print("="*100)

# Example 1: INNER JOIN - Get enrollments with student and course names
print("\n" + "="*100)
print("EXAMPLE 1: INNER JOIN - Students enrolled in courses")
print("="*100)
print("Shows only students who are enrolled in courses")
print("-"*100)

cur.execute("""
    SELECT 
        s.name AS student_name,
        s.mis_number,
        c.course_code,
        c.course_name,
        e.enrollment_date,
        e.status
    FROM enrollment e
    INNER JOIN student s ON e.student_id = s.id
    INNER JOIN course c ON e.course_id = c.id
    ORDER BY s.name
""")

rows = cur.fetchall()
if rows:
    for row in rows:
        print(f"Student: {row[0]} (MIS: {row[1]}) | Course: {row[2]} - {row[3]} | Date: {row[4]} | Status: {row[5]}")
else:
    print("No enrollments found.")

# Example 2: LEFT JOIN - All students, even if not enrolled
print("\n" + "="*100)
print("EXAMPLE 2: LEFT JOIN - All students (including those not enrolled)")
print("="*100)
print("Shows ALL students, even if they haven't enrolled in any course")
print("-"*100)

cur.execute("""
    SELECT 
        s.name AS student_name,
        s.mis_number,
        c.course_code,
        c.course_name,
        e.status
    FROM student s
    LEFT JOIN enrollment e ON s.id = e.student_id
    LEFT JOIN course c ON e.course_id = c.id
    ORDER BY s.name, c.course_code
""")

rows = cur.fetchall()
if rows:
    for row in rows:
        if row[2]:  # If course_code exists
            print(f"Student: {row[0]} (MIS: {row[1]}) | Course: {row[2]} - {row[3]} | Status: {row[4]}")
        else:
            print(f"Student: {row[0]} (MIS: {row[1]}) | Course: NOT ENROLLED")
else:
    print("No students found.")

# Example 3: RIGHT JOIN - All courses, even if no students enrolled
print("\n" + "="*100)
print("EXAMPLE 3: RIGHT JOIN - All courses (including those with no enrollments)")
print("="*100)
print("Shows ALL courses, even if no students have enrolled")
print("-"*100)

cur.execute("""
    SELECT 
        c.course_code,
        c.course_name,
        t.name AS teacher_name,
        COUNT(e.id) AS enrollment_count
    FROM enrollment e
    RIGHT JOIN course c ON e.course_id = c.id
    JOIN teacher t ON c.teacher_id = t.id
    GROUP BY c.id, c.course_code, c.course_name, t.name
    ORDER BY c.course_code
""")

rows = cur.fetchall()
if rows:
    for row in rows:
        print(f"Course: {row[0]} - {row[1]} | Teacher: {row[2]} | Enrollments: {row[3]}")
else:
    print("No courses found.")

# Example 4: Multiple JOINs - Complete enrollment details
print("\n" + "="*100)
print("EXAMPLE 4: MULTIPLE JOINs - Complete enrollment details with all info")
print("="*100)
print("Shows enrollment with student name, course name, and teacher name")
print("-"*100)

cur.execute("""
    SELECT 
        s.name AS student_name,
        c.course_code,
        c.course_name,
        t.name AS teacher_name,
        t.department,
        e.enrollment_date,
        e.grade,
        e.status
    FROM enrollment e
    JOIN student s ON e.student_id = s.id
    JOIN course c ON e.course_id = c.id
    JOIN teacher t ON c.teacher_id = t.id
    ORDER BY s.name, c.course_code
""")

rows = cur.fetchall()
if rows:
    for row in rows:
        grade_str = f", Grade: {row[6]}" if row[6] else ""
        print(f"Student: {row[0]} | Course: {row[1]} - {row[2]} | Teacher: {row[3]} ({row[4]}) | Date: {row[5]}{grade_str} | Status: {row[7]}")
else:
    print("No enrollments found.")

# Example 5: JOIN with WHERE clause - Filtered results
print("\n" + "="*100)
print("EXAMPLE 5: JOIN with WHERE - Only completed courses")
print("="*100)
print("Shows only enrollments with status = 'completed'")
print("-"*100)

cur.execute("""
    SELECT 
        s.name AS student_name,
        c.course_code,
        c.course_name,
        e.grade,
        e.enrollment_date
    FROM enrollment e
    JOIN student s ON e.student_id = s.id
    JOIN course c ON e.course_id = c.id
    WHERE e.status = 'completed'
    ORDER BY s.name
""")

rows = cur.fetchall()
if rows:
    for row in rows:
        print(f"Student: {row[0]} | Course: {row[1]} - {row[2]} | Grade: {row[3]} | Completed: {row[4]}")
else:
    print("No completed enrollments found.")

# Example 6: JOIN with aggregation - Count enrollments per student
print("\n" + "="*100)
print("EXAMPLE 6: JOIN with GROUP BY - Enrollment count per student")
print("="*100)
print("Shows how many courses each student is enrolled in")
print("-"*100)

cur.execute("""
    SELECT 
        s.name AS student_name,
        s.mis_number,
        COUNT(e.id) AS total_enrollments,
        COUNT(CASE WHEN e.status = 'completed' THEN 1 END) AS completed_courses,
        COUNT(CASE WHEN e.status = 'enrolled' THEN 1 END) AS active_courses
    FROM student s
    LEFT JOIN enrollment e ON s.id = e.student_id
    GROUP BY s.id, s.name, s.mis_number
    ORDER BY total_enrollments DESC, s.name
""")

rows = cur.fetchall()
if rows:
    for row in rows:
        print(f"Student: {row[0]} (MIS: {row[1]}) | Total: {row[2]} | Completed: {row[3]} | Active: {row[4]}")
else:
    print("No students found.")

# Example 7: JOIN with aggregation - Courses taught by each teacher
print("\n" + "="*100)
print("EXAMPLE 7: JOIN with GROUP BY - Courses per teacher")
print("="*100)
print("Shows how many courses each teacher teaches")
print("-"*100)

cur.execute("""
    SELECT 
        t.name AS teacher_name,
        t.department,
        COUNT(c.id) AS total_courses,
        COUNT(e.id) AS total_enrollments,
        STRING_AGG(c.course_code, ', ') AS courses
    FROM teacher t
    LEFT JOIN course c ON t.id = c.teacher_id
    LEFT JOIN enrollment e ON c.id = e.course_id
    GROUP BY t.id, t.name, t.department
    ORDER BY t.name
""")

rows = cur.fetchall()
if rows:
    for row in rows:
        courses_str = row[4] if row[4] else "No courses"
        print(f"Teacher: {row[0]} ({row[1]}) | Courses: {row[2]} | Total Enrollments: {row[3]} | Course Codes: {courses_str}")
else:
    print("No teachers found.")

print("\n" + "="*100)
print("END OF JOIN EXAMPLES")
print("="*100)

# Close the connection
cur.close()
conn.close()

