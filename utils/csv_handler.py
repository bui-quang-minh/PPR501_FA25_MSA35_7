import csv
from models.student import Student


class CSVHandler:
    @staticmethod
    def import_from_csv(filename):
        students = []
        with open(filename, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                student = Student(
                    row['StudentID'].strip(),
                    row['LastName'].strip(),
                    row['FirstName'].strip(),
                    row['DOB'].strip(),
                    row['Address'].strip() if row.get('Address') else '',
                    float(row['MathGrade']) if row.get('MathGrade') and row['MathGrade'].strip() else None,
                    float(row['LiteratureGrade']) if row.get('LiteratureGrade') and row['LiteratureGrade'].strip() else None,
                    float(row['EnglishGrade']) if row.get('EnglishGrade') and row['EnglishGrade'].strip() else None
                )
                students.append(student)
        return students

    @staticmethod
    def export_to_csv(filename, students):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['StudentID', 'LastName', 'FirstName', 'DOB',
                                 'Address', 'MathGrade', 'LiteratureGrade', 'EnglishGrade'])
            for student in students:
                csv_writer.writerow(student.to_tuple())