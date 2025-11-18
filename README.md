# PostgreSQL Student Management System

This project demonstrates how to connect to PostgreSQL database and perform CRUD operations with image storage.

## Features

- Connect to PostgreSQL database
- Insert student records with image data
- Check for duplicate MIS numbers
- Fetch and display all student records
- Error handling for database operations and file operations

## Prerequisites

- Python 3.7 or higher
- PostgreSQL database installed and running
- A database named `COEP` created
- A `student` table created with the following schema:

```sql
CREATE TABLE student (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    mis_number VARCHAR(50) UNIQUE NOT NULL,
    age INTEGER NOT NULL,
    city VARCHAR(100),
    image_path VARCHAR(500),
    image_data BYTEA
);
```

## Installation

1. Install the required Python package:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the `postgresqlDB` folder (you can copy from `env.example`):
```bash
cp env.example .env
```

2. Edit the `.env` file with your actual PostgreSQL credentials:
```env
POSTGRES_DB=COEP
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

**Important:** Replace `your_username` and `your_password` with your actual PostgreSQL username and password.

The script will automatically load these credentials from the `.env` file.

## Usage

Run the script:
```bash
python postgresDB.py
```

The script will prompt you to enter:
- Student name
- MIS number (must be unique)
- Age
- City
- Image path (path to the image file on your system)

After inserting the data, it will display all student records in the database.

## Database Schema

The `student` table should have the following columns:
- `id`: Auto-incrementing primary key
- `name`: Student's name (VARCHAR)
- `mis_number`: Unique MIS number (VARCHAR, UNIQUE)
- `age`: Student's age (INTEGER)
- `city`: Student's city (VARCHAR)
- `image_path`: Path to the image file (VARCHAR)
- `image_data`: Binary image data (BYTEA)

## Error Handling

The script includes error handling for:
- Database connection errors
- Duplicate MIS number detection
- Missing image files
- Invalid input validation
- Database operation errors

## Notes

- The MIS number must be unique. If you try to insert a duplicate MIS number, the script will display an error message.
- The image file path must be valid and the file must exist.
- Image data is stored as binary (BYTEA) in PostgreSQL.

