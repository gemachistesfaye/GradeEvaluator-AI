import sqlite3
from datetime import datetime

DATABASE = 'gradeevaluator.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                joined_date TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject TEXT NOT NULL,
                score REAL NOT NULL,
                letter_grade TEXT NOT NULL,
                gpa_points REAL NOT NULL,
                ai_feedback TEXT,
                date TEXT NOT NULL,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        ''')
        conn.commit()

def create_student(name, email, password_hash, joined_date):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO students (name, email, password_hash, joined_date) VALUES (?, ?, ?, ?)",
            (name, email, password_hash, joined_date)
        )
        conn.commit()

def get_student_by_email(email):
    with get_db() as conn:
        user = conn.execute("SELECT * FROM students WHERE email = ?", (email,)).fetchone()
        return dict(user) if user else None

def get_student_by_id(student_id):
    with get_db() as conn:
        user = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
        return dict(user) if user else None

def update_user_password(user_id, new_password_hash):
    with get_db() as conn:
        conn.execute("UPDATE students SET password_hash = ? WHERE id = ?", (new_password_hash, user_id))
        conn.commit()

def get_user_profile(user_id):
    return get_student_by_id(user_id)

def get_grade_count(user_id):
    with get_db() as conn:
        count = conn.execute("SELECT COUNT(*) FROM grades WHERE student_id = ?", (user_id,)).fetchone()
        return count[0] if count else 0

def add_grade(student_id, subject, score, letter_grade, gpa_points, ai_feedback):
    date_str = datetime.now().strftime("%B %d, %Y")
    with get_db() as conn:
        conn.execute(
            "INSERT INTO grades (student_id, subject, score, letter_grade, gpa_points, ai_feedback, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (student_id, subject, score, letter_grade, gpa_points, ai_feedback, date_str)
        )
        conn.commit()

def get_grades_by_student(student_id):
    with get_db() as conn:
        grades = conn.execute("SELECT * FROM grades WHERE student_id = ? ORDER BY id DESC", (student_id,)).fetchall()
        return [dict(g) for g in grades]

def delete_grade(grade_id, student_id):
    with get_db() as conn:
        conn.execute("DELETE FROM grades WHERE id = ? AND student_id = ?", (grade_id, student_id))
        conn.commit()

def clear_grades(student_id):
    with get_db() as conn:
        conn.execute("DELETE FROM grades WHERE student_id = ?", (student_id,))
        conn.commit()
