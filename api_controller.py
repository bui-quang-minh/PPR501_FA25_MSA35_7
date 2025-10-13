from fastapi import FastAPI, HTTPException
import database.db_manager as db_manager
from pydantic import BaseModel
from typing import List
import sqlite3


API_URL = "http://127.0.0.1:8000"

app = FastAPI()
db = db_manager.DatabaseManager()


@app.get("/students")
def get_students(top: int = None):
    try:
        if top is not None:
            students = db.get_top_n_students(top)
        else:
            students = db.get_all_students()
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

