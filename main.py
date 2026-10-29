"""Student Management System - Python + MySQL CRUD CLI."""
import os
from getpass import getpass

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


class StudentManagementSystem:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=int(os.getenv("DB_PORT", "3306")),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", ""),
                database=os.getenv("DB_NAME", "student_management"),
            )
            if self.connection.is_connected():
                return True
        except Error as exc:
            print(f"\nDatabase connection failed: {exc}")
            print("Check MySQL is running and your .env settings are correct.")
        return False

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    @staticmethod
    def read_nonempty(prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("This field cannot be empty.")

    @staticmethod
    def read_email():
        while True:
            email = input("Email: ").strip()
            if "@" in email and "." in email.rsplit("@", 1)[-1]:
                return email
            print("Enter a valid email address.")

    def add_student(self):
        print("\n--- Add Student ---")
        name = self.read_nonempty("Full name: ")
        age_text = self.read_nonempty("Age: ")
        try:
            age = int(age_text)
            if not 1 <= age <= 120:
                raise ValueError
        except ValueError:
            print("Age must be a whole number between 1 and 120.")
            return
        email = self.read_email()
        course = self.read_nonempty("Course: ")
        sql = """INSERT INTO students (name, age, email, course)
                 VALUES (%s, %s, %s, %s)"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (name, age, email, course))
            self.connection.commit()
            print("Student added successfully.")
        except Error as exc:
            self.connection.rollback()
            print(f"Could not add student: {exc}")

    def view_students(self):
        print("\n--- Student Records ---")
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "SELECT id, name, age, email, course, created_at "
                    "FROM students ORDER BY id"
                )
                students = cursor.fetchall()
            if not students:
                print("No student records found.")
                return
            print("-" * 105)
            print(f"{'ID':<5}{'NAME':<24}{'AGE':<7}{'EMAIL':<32}{'COURSE':<22}{'CREATED'}")
            print("-" * 105)
            for s in students:
                created = str(s["created_at"])[:19] if s["created_at"] else ""
                print(
                    f"{s['id']:<5}{s['name'][:22]:<24}{s['age']:<7}"
                    f"{s['email'][:30]:<32}{s['course'][:20]:<22}{created}"
                )
            print("-" * 105)
        except Error as exc:
            print(f"Could not retrieve students: {exc}")

    def update_student(self):
        print("\n--- Update Student ---")
        try:
            student_id = int(self.read_nonempty("Student ID to update: "))
            if student_id < 1:
                raise ValueError
        except ValueError:
            print("Enter a valid positive student ID.")
            return

        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
            student = cursor.fetchone()
        if not student:
            print("No student found with that ID.")
            return

        print("Press Enter to keep the current value.")
        name = input(f"Name [{student['name']}]: ").strip() or student["name"]
        age_text = input(f"Age [{student['age']}]: ").strip()
        email = input(f"Email [{student['email']}]: ").strip() or student["email"]
        course = input(f"Course [{student['course']}]: ").strip() or student["course"]

        try:
            age = int(age_text) if age_text else student["age"]
            if not 1 <= age <= 120:
                raise ValueError
            if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
                raise ValueError("Invalid email")
            sql = """UPDATE students
                     SET name=%s, age=%s, email=%s, course=%s
                     WHERE id=%s"""
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (name, age, email, course, student_id))
            self.connection.commit()
            print("Student updated successfully.")
        except ValueError:
            print("Invalid age or email. No changes were saved.")
        except Error as exc:
            self.connection.rollback()
            print(f"Could not update student: {exc}")

    def delete_student(self):
        print("\n--- Delete Student ---")
        try:
            student_id = int(self.read_nonempty("Student ID to delete: "))
            if student_id < 1:
                raise ValueError
        except ValueError:
            print("Enter a valid positive student ID.")
            return

        with self.connection.cursor() as cursor:
            cursor.execute("SELECT name FROM students WHERE id = %s", (student_id,))
            result = cursor.fetchone()
        if not result:
            print("No student found with that ID.")
            return

        confirm = input(f"Delete {result[0]}? Type YES to confirm: ").strip()
        if confirm != "YES":
            print("Delete cancelled.")
            return
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            self.connection.commit()
            print("Student deleted successfully.")
        except Error as exc:
            self.connection.rollback()
            print(f"Could not delete student: {exc}")

    def search_student(self):
        print("\n--- Search Students ---")
        keyword = self.read_nonempty("Search by name, email, or course: ")
        pattern = f"%{keyword}%"
        sql = """SELECT id, name, age, email, course
                 FROM students
                 WHERE name LIKE %s OR email LIKE %s OR course LIKE %s
                 ORDER BY id"""
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(sql, (pattern, pattern, pattern))
                results = cursor.fetchall()
            if not results:
                print("No matching students found.")
                return
            for s in results:
                print(
                    f"ID: {s['id']} | Name: {s['name']} | Age: {s['age']} | "
                    f"Email: {s['email']} | Course: {s['course']}"
                )
        except Error as exc:
            print(f"Search failed: {exc}")

    def run(self):
        if not self.connect():
            return
        actions = {
            "1": self.add_student,
            "2": self.view_students,
            "3": self.update_student,
            "4": self.delete_student,
            "5": self.search_student,
        }
        try:
            while True:
                print("\n====== STUDENT MANAGEMENT SYSTEM ======")
                print("1. Add student")
                print("2. View all students")
                print("3. Update student")
                print("4. Delete student")
                print("5. Search students")
                print("0. Exit")
                choice = input("Choose an option: ").strip()
                if choice == "0":
                    print("Goodbye!")
                    break
                action = actions.get(choice)
                if action:
                    action()
                else:
                    print("Invalid choice. Select 0 to 5.")
        finally:
            self.close()


if __name__ == "__main__":
    StudentManagementSystem().run()
