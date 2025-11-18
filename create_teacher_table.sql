-- SQL script to create the teacher table in PostgreSQL

CREATE TABLE IF NOT EXISTS teacher (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    department VARCHAR(100),
    phone VARCHAR(20)
);

-- Create an index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_teacher_email ON teacher(email);

-- Add comments to the table
COMMENT ON TABLE teacher IS 'Table to store teacher information';
COMMENT ON COLUMN teacher.email IS 'Unique email address for each teacher';

