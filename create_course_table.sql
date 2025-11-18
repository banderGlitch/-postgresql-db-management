-- SQL script to create the course table in PostgreSQL

CREATE TABLE IF NOT EXISTS course (
    id SERIAL PRIMARY KEY,
    course_code VARCHAR(50) UNIQUE NOT NULL,
    course_name VARCHAR(255) NOT NULL,
    teacher_id INTEGER NOT NULL,
    credits INTEGER NOT NULL,
    description TEXT,
    FOREIGN KEY (teacher_id) REFERENCES teacher(id) ON DELETE CASCADE
);

-- Create an index on course_code for faster lookups
CREATE INDEX IF NOT EXISTS idx_course_code ON course(course_code);

-- Create an index on teacher_id for faster joins
CREATE INDEX IF NOT EXISTS idx_course_teacher_id ON course(teacher_id);

-- Add comments to the table
COMMENT ON TABLE course IS 'Table to store course information';
COMMENT ON COLUMN course.teacher_id IS 'Foreign key reference to teacher table';
COMMENT ON COLUMN course.course_code IS 'Unique course code identifier';

