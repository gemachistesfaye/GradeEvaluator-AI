import sqlite3
from datetime import datetime

DB_NAME = "gradeevaluator.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            joined_date TEXT NOT NULL
        )
    ''')

    # Grades table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            score REAL NOT NULL,
            letter_grade TEXT NOT NULL,
            gpa_points REAL NOT NULL,
            ai_feedback TEXT,
            date TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init_db()
