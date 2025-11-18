-- SQL script to create the enrollment table in PostgreSQL

CREATE TABLE IF NOT EXISTS enrollment (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrollment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    grade VARCHAR(10),
    status VARCHAR(20) DEFAULT 'enrolled' CHECK (status IN ('enrolled', 'completed', 'dropped')),
    FOREIGN KEY (student_id) REFERENCES student(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE,
    UNIQUE(student_id, course_id)
);

-- Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_enrollment_student_id ON enrollment(student_id);
CREATE INDEX IF NOT EXISTS idx_enrollment_course_id ON enrollment(course_id);
CREATE INDEX IF NOT EXISTS idx_enrollment_status ON enrollment(status);

-- Add comments to the table
COMMENT ON TABLE enrollment IS 'Table to store student course enrollments';
COMMENT ON COLUMN enrollment.student_id IS 'Foreign key reference to student table';
COMMENT ON COLUMN enrollment.course_id IS 'Foreign key reference to course table';
COMMENT ON COLUMN enrollment.status IS 'Enrollment status: enrolled, completed, or dropped';

