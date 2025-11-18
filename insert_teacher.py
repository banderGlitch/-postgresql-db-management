"""
Script to insert teacher data into the database
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
name = input("Enter teacher name: ")
email = input("Enter teacher email: ")
department = input("Enter department: ")
phone = input("Enter phone (optional, press Enter to skip): ")

# Insert data into the teacher table
try:
    cur.execute("""
        INSERT INTO teacher (name, email, department, phone)
        VALUES (%s, %s, %s, %s)
    """, (name, email, department, phone if phone else None))
    
    # Commit the changes
    conn.commit()
    print(f"✓ Teacher {name} inserted successfully!")
except psycopg2.IntegrityError:
    print("✗ Error: Email already exists!")
    conn.rollback()

# Close the connection
cur.close()
conn.close()

