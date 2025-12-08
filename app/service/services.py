from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud import get_student_info, get_group_info, update_student

from app.exceptions.exceptions import NotFoundError, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

async def add_student_to_group(db: AsyncSession, student_id: int, group_id: int):
    student = await get_student_info(db, student_id)
    if not student:
        raise NotFoundError("Студент не найден")

    group = await get_group_info(db, group_id)
    if not group:
        raise NotFoundError("Группа не найдена")

    if student.group_id == group_id:
        raise ValidationError("Студент уже состоит в этой группе")

    updated_student = await update_student(db, student_id, {"group_id": group_id})
    return updated_student


async def delete_student_from_group(db: AsyncSession, group_id: int, student_id: int):
    student = await get_student_info(db, student_id)
    if not student:
        raise NotFoundError("Студент не найден")

    group = await get_group_info(db, group_id)
    if not group:
        raise NotFoundError("Группа не найдена")
    
    if student.group_id is None:
        raise ValidationError("Студент уже не состоит ни в одной группе")

    updated_student = await update_student(db, student_id, {"group_id": None})
    return updated_student


async def transfer_student(db: AsyncSession, student_id: int, new_group_id: int):
    student = await get_student_info(db, student_id)
    if not student:
        raise NotFoundError("Студент не найден")

    new_group = await get_group_info(db, new_group_id)
    if not new_group:
        raise NotFoundError("Группа не найдена")

    if student.group_id == new_group_id:
        raise ValidationError("Студент уже состоит в этой группе")

    updated_student = await update_student(db, student_id, {"group_id": new_group_id})
    return updated_student
