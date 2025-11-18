"""
Script to create the teacher table in PostgreSQL
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

# Read and execute the SQL file
with open('create_teacher_table.sql', 'r') as sql_file:
    sql_script = sql_file.read()
    cur.execute(sql_script)
    conn.commit()

print("✓ Teacher table created successfully!")

cur.close()
conn.close()

