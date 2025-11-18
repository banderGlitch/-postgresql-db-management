"""
Script to populate all tables with sample data in correct order
"""

import subprocess
import sys

print("="*80)
print("POPULATING ALL TABLES WITH SAMPLE DATA")
print("="*80)

# Step 1: Populate students
print("\n1. Populating Student table...")
print("-"*80)
subprocess.run([sys.executable, 'populate_student_data.py'])

# Step 2: Populate teachers
print("\n2. Populating Teacher table...")
print("-"*80)
subprocess.run([sys.executable, 'populate_teacher_data.py'])

# Step 3: Populate courses
print("\n3. Populating Course table...")
print("-"*80)
subprocess.run([sys.executable, 'populate_course_data.py'])

# Step 4: Populate enrollments
print("\n4. Populating Enrollment table...")
print("-"*80)
subprocess.run([sys.executable, 'populate_enrollment_data.py'])

print("\n" + "="*80)
print("✓ All tables populated successfully!")
print("="*80)

