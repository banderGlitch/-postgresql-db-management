"""
Grant permissions to testuser for creating tables
"""

import psycopg2  # pyright: ignore[reportMissingModuleSource]
import os
from dotenv import load_dotenv

load_dotenv()

# Connect as postgres user (superuser) to grant permissions
conn = psycopg2.connect(
    dbname=os.getenv('POSTGRES_DB', 'COEP'),
    user='postgres',  # Use postgres user to grant permissions
    password=input("Enter postgres password: "),  # You'll need to enter postgres password
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=os.getenv('POSTGRES_PORT', '5432')
)

cur = conn.cursor()

dbname = os.getenv('POSTGRES_DB', 'COEP')
username = os.getenv('POSTGRES_USER', 'postgres')

# Grant permissions
cur.execute(f'GRANT ALL ON SCHEMA public TO {username};')
cur.execute(f'GRANT CREATE ON SCHEMA public TO {username};')
cur.execute(f'ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO {username};')

conn.commit()
print(f"✓ Permissions granted to {username} successfully!")

cur.close()
conn.close()

