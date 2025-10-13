from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.student import Student, Base


class DatabaseManager:
    def __init__(self, db_name='students.db'):
        self.db_name = db_name
        self.engine = create_engine(f'sqlite:///{db_name}')
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.session = None
        self.create_table()

    def create_table(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        if self.session is None:
            self.session = self.Session()
        return self.session

    def add_student(self, student):
        session = self.get_session()
        session.add(student)
        session.commit()

    def get_all_students(self):
        session = self.get_session()
        return session.query(Student).order_by(Student.student_id).all()

    def get_student_by_id(self, student_id):
        session = self.get_session()
        return session.query(Student).filter(Student.student_id == student_id).first()

    def update_student(self, student):
        session = self.get_session()
        existing_student = session.query(Student).filter(
            Student.student_id == student.student_id
        ).first()

        if existing_student:
            existing_student.lastname = student.lastname
            existing_student.firstname = student.firstname
            existing_student.dob = student.dob
            existing_student.address = student.address
            existing_student.math_grade = student.math_grade
            existing_student.literature_grade = student.literature_grade
            existing_student.english_grade = student.english_grade
            session.commit()

    def delete_student(self, student_id):
        session = self.get_session()
        student = session.query(Student).filter(Student.student_id == student_id).first()
        if student:
            session.delete(student)
            session.commit()

    def import_students(self, students):
        session = self.get_session()
        for student in students:
            session.merge(student)
        session.commit()

    def close(self):
        if self.session:
            self.session.close()
        self.Session.remove()