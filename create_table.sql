-- SQL script to create the student table in PostgreSQL

CREATE TABLE IF NOT EXISTS student (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    mis_number VARCHAR(50) UNIQUE NOT NULL,
    age INTEGER NOT NULL,
    city VARCHAR(100),
    image_path VARCHAR(500),
    image_data BYTEA
);

-- Create an index on mis_number for faster lookups
CREATE INDEX IF NOT EXISTS idx_mis_number ON student(mis_number);

-- Add comments to the table
COMMENT ON TABLE student IS 'Table to store student information with image data';
COMMENT ON COLUMN student.mis_number IS 'Unique MIS (Management Information System) number for each student';
COMMENT ON COLUMN student.image_data IS 'Binary image data stored as BYTEA';




