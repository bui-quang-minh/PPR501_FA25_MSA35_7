import sqlite3
from models.student import Student


class DatabaseManager:
    def __init__(self, db_name='students.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                lastname TEXT NOT NULL,
                firstname TEXT NOT NULL,
                dob TEXT NOT NULL,
                address TEXT NOT NULL,
                math_grade REAL,
                literature_grade REAL,
                english_grade REAL
            )
        ''')
        self.conn.commit()

    def add_student(self, student):
        self.cursor.execute('''
            INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', student.to_tuple())
        self.conn.commit()

    def get_all_students(self):
        self.cursor.execute('SELECT * FROM students ORDER BY student_id')
        rows = self.cursor.fetchall()
        return [Student.from_tuple(row) for row in rows]

    def get_student_by_id(self, student_id):
        self.cursor.execute('SELECT * FROM students WHERE student_id=?', (student_id,))
        row = self.cursor.fetchone()
        return Student.from_tuple(row) if row else None

    def update_student(self, student):
        self.cursor.execute('''
            UPDATE students SET 
                lastname=?, firstname=?, dob=?, address=?, 
                math_grade=?, literature_grade=?, english_grade=?
            WHERE student_id=?
        ''', (
            student.lastname,
            student.firstname,
            student.dob,
            student.address,
            student.math_grade,
            student.literature_grade,
            student.english_grade,
            student.student_id
        ))
        self.conn.commit()

    def delete_student(self, student_id):
        self.cursor.execute('DELETE FROM students WHERE student_id=?', (student_id,))
        self.conn.commit()

    def import_students(self, students):
        for student in students:
            self.cursor.execute('''
                INSERT OR REPLACE INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', student.to_tuple())
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()