from fastapi import FastAPI, HTTPException
from database.db_manager import DatabaseManager
from models.student import Student
from pydantic import BaseModel, Field
from typing import List, Optional


API_URL = "http://127.0.0.1:8000"

app = FastAPI(title="Student Management API", version="1.0.0")
db = DatabaseManager()

class StudentCreate(BaseModel):
    student_id: str = Field(..., description="Student ID")
    lastname: str = Field(..., min_length=1, description="Last name")
    firstname: str = Field(..., min_length=1, description="First name")
    dob: str = Field(..., description="Date of birth")
    address: str = Field(..., min_length=1, description="Address")
    math_grade: Optional[float] = Field(None, ge=0, le=10, description="Math grade (0-10)")
    literature_grade: Optional[float] = Field(None, ge=0, le=10, description="Literature grade (0-10)")
    english_grade: Optional[float] = Field(None, ge=0, le=10, description="English grade (0-10)")


class StudentResponse(BaseModel):
    student_id: str
    lastname: str
    firstname: str
    dob: str
    address: str
    math_grade: Optional[float]
    literature_grade: Optional[float]
    english_grade: Optional[float]

    class Config:
        from_attributes = True


@app.get("/")
def health_check():
    return {"status": "online", "message": "Student Management API is running"}


@app.get("/students", response_model=List[StudentResponse])
def get_students(top: Optional[int] = None):
    try:
        if top is not None:
            students = db.get_top_n_students(top)
        else:
            students = db.get_all_students()

        result = []
        for student in students:
            student_dict = {
                "student_id": student.student_id,
                "lastname": student.lastname,
                "firstname": student.firstname,
                "dob": student.dob,
                "address": student.address,
                "math_grade": student.math_grade,
                "literature_grade": student.literature_grade,
                "english_grade": student.english_grade
            }
            result.append(student_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/all_students")
#getall
def get_students():
    try:
        students = db.get_all_students()
        result = []
        for student in students:
            student_dict = {
                "student_id": student.student_id,
                "lastname": student.lastname,
                "firstname": student.firstname,
                "dob": student.dob,
                "address": student.address,
                "math_grade": student.math_grade,
                "literature_grade": student.literature_grade,
                "english_grade": student.english_grade
            }
            result.append(student_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: str):
    try:
        student = db.get_student_by_id(student_id)
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")

        student_dict = {
            "student_id": student.student_id,
            "lastname": student.lastname,
            "firstname": student.firstname,
            "dob": student.dob,
            "address": student.address,
            "math_grade": student.math_grade,
            "literature_grade": student.literature_grade,
            "english_grade": student.english_grade
        }

        return student_dict
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/students", status_code=201)
def create_student(student_data: StudentCreate):
    try:
        existing_student = db.get_student_by_id(student_data.student_id)
        if existing_student is not None:
            raise HTTPException(status_code=409, detail="Student with this ID already exists")

        student = Student(
            student_id=student_data.student_id,
            lastname=student_data.lastname,
            firstname=student_data.firstname,
            dob=student_data.dob,
            address=student_data.address,
            math_grade=student_data.math_grade,
            literature_grade=student_data.literature_grade,
            english_grade=student_data.english_grade
        )

        db.add_student(student)
        return {"message": f"Student {student_data.student_id} created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/students/{student_id}")
def update_student(student_id: str, student_data: StudentCreate):
    try:
        existing_student = db.get_student_by_id(student_id)
        if existing_student is None:
            raise HTTPException(status_code=404, detail="Student not found")

        student = Student(
            student_id=student_data.student_id,
            lastname=student_data.lastname,
            firstname=student_data.firstname,
            dob=student_data.dob,
            address=student_data.address,
            math_grade=student_data.math_grade,
            literature_grade=student_data.literature_grade,
            english_grade=student_data.english_grade
        )

        db.update_student(student)
        return {"message": f"Student {student_id} updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    try:
        existing_student = db.get_student_by_id(student_id)
        if existing_student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        db.delete_student(student_id)
        return {"message": f"Student {student_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.get("/search", response_model=List[StudentResponse])
def search_students(query: str):
    try:
        if not query or len(query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Search query cannot be empty")

        students = db.get_all_students()
        query_lower = query.lower().strip()
        matching_students = []

        for student in students:
            if (query_lower in student.student_id.lower() or
                query_lower in student.firstname.lower() or
                query_lower in student.lastname.lower()):

                student_dict = {
                    "student_id": student.student_id,
                    "lastname": student.lastname,
                    "firstname": student.firstname,
                    "dob": student.dob,
                    "address": student.address,
                    "math_grade": student.math_grade,
                    "literature_grade": student.literature_grade,
                    "english_grade": student.english_grade
                }

                matching_students.append(student_dict)

        return matching_students
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))