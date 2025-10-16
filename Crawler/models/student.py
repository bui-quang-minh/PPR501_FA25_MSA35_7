class Student:
    def __init__(self, student_id, lastname, firstname, dob, address,
                 math_grade=None, literature_grade=None, english_grade=None):
        self.student_id = student_id
        self.lastname = lastname
        self.firstname = firstname
        self.dob = dob
        self.address = address
        self.math_grade = math_grade
        self.literature_grade = literature_grade
        self.english_grade = english_grade

    def to_tuple(self):
        return (
            self.student_id,
            self.lastname,
            self.firstname,
            self.dob,
            self.address,
            self.math_grade,
            self.literature_grade,
            self.english_grade
        )

    def __repr__(self):
        return f"Student Info({self.student_id}, {self.lastname}, {self.firstname}, {self.dob}, {self.address}, {self.math_grade}, {self.literature_grade}, {self.english_grade})\n"