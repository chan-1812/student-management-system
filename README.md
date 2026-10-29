# Student Management System

A command-line student record management application built with **Python, Object-Oriented Programming (OOP), and MySQL**.

## Features

- Add student records
- View all student records
- Update existing records
- Delete records after confirmation
- Search by name, email, or course
- Input validation and exception handling
- Parameterized SQL queries to help prevent SQL injection
- Environment-based database configuration (credentials are not stored in source code)

## Requirements

- Python 3.9+
- MySQL Server
- pip

## Setup

### 1. Create the database and table

Open MySQL Workbench or the MySQL command-line client and run the contents of `schema.sql`.

### 2. Create and activate a virtual environment (recommended)

Windows:

```bash
python -m venv .venv
.venv\\Scripts\\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

Copy `.env.example` to `.env` and update the values for your local MySQL setup.

Windows Command Prompt:

```bat
copy .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Never commit your real `.env` file or database password to GitHub.

### 5. Run the application

```bash
python main.py
```

Choose an option from the menu to create, view, update, delete, or search student records.

## Database fields

| Field | Description |
|---|---|
| `id` | Auto-incrementing primary key |
| `name` | Student's full name |
| `age` | Student's age |
| `email` | Unique email address |
| `course` | Student's course |
| `created_at` | Record creation timestamp |

## Project structure

```text
student_management_system/
├── main.py
├── schema.sql
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Troubleshooting

- **Access denied:** Verify `DB_USER` and `DB_PASSWORD` in `.env`.
- **Unknown database:** Run `schema.sql` in MySQL.
- **Connection refused:** Start the MySQL service and check `DB_HOST` and `DB_PORT`.
- **Duplicate email:** Each student must have a unique email address.

## Skills demonstrated

Python, OOP, MySQL, SQL, CRUD operations, input validation, exception handling, database connectivity, Git, and GitHub.

> This is a local learning project. Test it with sample data before using it for real student records.
