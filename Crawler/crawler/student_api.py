import requests
from requests.exceptions import RequestException
from models.student import Student
import xmltodict

class StudentApi:
    def __init__(self, api_url='http://127.0.0.1:8000'):
        self.api_url = api_url


    def fetch_all_students(self):
        try:
            response = requests.get(f"{self.api_url}/students")
            response.raise_for_status()
            print("Response Text:", response.text)
            xml_dict = xmltodict.parse(response.text)
            print("Dict:", xml_dict)
            items = xml_dict.get("students", {}).get("item", [])
            print(items)

            students = []
            for data in items:
                student = Student(
                    student_id=data.get("student_id"),
                    lastname=data.get("lastname"),
                    firstname=data.get("firstname"),
                    dob=data.get("dob"),
                    address=data.get("address"),
                    math_grade=float(data.get("math_grade")) if data.get("math_grade") else None,
                    literature_grade=float(data.get("literature_grade")) if data.get("literature_grade") else None,
                    english_grade=float(data.get("english_grade")) if data.get("english_grade") else None
                )
                students.append(student)

            return students
        except RequestException as e:
            print(f"Error fetching data from API: {e}")
            return []