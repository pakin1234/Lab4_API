# students_api.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.schemas import StudentResponse, StudentCreate, StudentUpdate
from app.crud.crud import get_all_students_info, get_student_info, create_student, update_student, delete_student
from app.db.database import get_db

students = APIRouter(prefix="/students", tags=["Students"])

@students.get("/", response_model=list[StudentResponse])
async def get_all_students_api(db: AsyncSession = Depends(get_db)):
    return await get_all_students_info(db)

@students.get("/{student_id}", response_model=StudentResponse)
async def get_student_info_api(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await get_student_info(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@students.post("/new", response_model=StudentResponse)
async def create_student_api(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    return await create_student(db, student)

@students.put("/{student_id}", response_model=StudentResponse)
async def update_student_api(student_id: int, updated_data: StudentUpdate, db: AsyncSession = Depends(get_db)):
    student = await update_student(db, student_id, updated_data.model_dump())
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@students.delete("/{student_id}", response_model=StudentResponse)
async def delete_student_api(student_id: int, db: AsyncSession = Depends(get_db)):
    deleted_student = await delete_student(db, student_id)
    if deleted_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return deleted_student




