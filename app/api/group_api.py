# group_api.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.schemas import GroupBase, GroupWithStudents, GroupResponse, GroupCreate, StudentResponse
from app.crud.crud import get_all_groups, get_group_info, delete_group, create_group, get_students_from_group
from app.service.services import add_student_to_group, delete_student_from_group, transfer_student
from app.exceptions.exceptions import NotFoundError, ValidationError
from app.db.database import get_db

groups = APIRouter(prefix="/group", tags=["Group"])

@groups.get("/", response_model=list[GroupWithStudents])
async def get_all_groups_api(db: AsyncSession = Depends(get_db)):
    return await get_all_groups(db)

@groups.get("/{group_id}", response_model=GroupWithStudents)
async def get_group_info_api(group_id: int, db: AsyncSession = Depends(get_db)):
    group = await get_group_info(db, group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@groups.post("/new", response_model=GroupResponse)
async def create_new_group_api(group: GroupCreate, db: AsyncSession = Depends(get_db)):
    return await create_group(db, group)

@groups.delete("/{group_id}", response_model=GroupBase)
async def delete_group_api(group_id: int, db: AsyncSession = Depends(get_db)):
    deleted_group = await delete_group(db, group_id)
    if deleted_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return deleted_group

@groups.get("/{group_id}/students", response_model=list[StudentResponse])
async def get_students_from_group_api(group_id: int, db: AsyncSession = Depends(get_db)):
    return await get_students_from_group(db, group_id)

@groups.put("/{group_id}/add/student/{student_id}", response_model=StudentResponse)
async def add_student_to_group_api(group_id: int, student_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await add_student_to_group(db, student_id, group_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@groups.post("/{student_id}/transfer/{new_group_id}", response_model=StudentResponse)
async def transfer_student_api(student_id: int, new_group_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await transfer_student(db, student_id, new_group_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@groups.put("/{group_id}/delete/students/{student_id}", response_model=StudentResponse)
async def delete_student_from_group_api(group_id: int,student_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await delete_student_from_group(db, group_id, student_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))