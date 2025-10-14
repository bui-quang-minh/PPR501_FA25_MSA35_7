from datetime import datetime


class Validator:
    @staticmethod
    def validate_student_id(student_id):
        if not student_id or not student_id.strip():
            return False, "Student ID is required"
        return True, ""

    @staticmethod
    def validate_name(name, field_name):
        if not name or not name.strip():
            return False, f"{field_name} is required"
        return True, ""

    @staticmethod
    def validate_dob(dob):
        try:
            datetime.strptime(dob, '%d-%m-%y')
            return True, ""
        except ValueError:
            return False, "Date format must be DD-MM-YYYY"

    @staticmethod
    def validate_grade(grade):
        if not grade or not grade.strip():
            return True, ""
        try:
            g = float(grade)
            if 0 <= g <= 100:
                return True, ""
            return False, "Grade must be between 0 and 100"
        except ValueError:
            return False, "Grade must be a number"
