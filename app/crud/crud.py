from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models import Student, Group
from app.schemas.schemas import StudentCreate, GroupCreate

async def get_all_students_info(db: AsyncSession) -> list[Student]:
    '''Получить список студентов'''
    result = await db.execute(select(Student))
    students = result.scalars().all()
    return students

async def get_student_info(db: AsyncSession, student_id: int) -> Student:
    '''Получить информацию о студенте по его id'''
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        return None
    return student

async def delete_student(db: AsyncSession, student_id: int) -> Student | None:
    '''Удалить студента'''
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        return None
    await db.delete(student)
    await db.commit()
    return student
    
async def get_all_groups(db: AsyncSession) -> list[Group]:
    '''Получить список групп'''
    groups = await db.execute(select(Group).options(selectinload(Group.students)))
    return groups.scalars().all()

async def get_group_info(db: AsyncSession, group_id: int) -> Group:
    '''Получить информацию о группе по ее id'''
    result = await db.execute(select(Group).where(Group.id == group_id).options(selectinload(Group.students)))
    group = result.scalar_one_or_none() 
    return group

async def delete_group(db: AsyncSession, group_id: int) -> Group | None:
    '''Удалить группу'''
    result = await db.execute(select(Group).where(Group.id == group_id))
    group = result.scalar_one_or_none()
    if group is None:
        return None
    await db.delete(group)
    await db.commit()
    return group

async def get_students_from_group(db: AsyncSession, group_id: int) -> list[Student]:
    '''Получить всех студентов в группе'''
    students = await db.execute(select(Student).where(Student.group_id == group_id))
    return students.scalars().all()

async def create_student(db: AsyncSession, student_create: StudentCreate) -> Student:
    '''Создать студента '''
    student = Student(**student_create.model_dump())
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student

async def create_group(db: AsyncSession, group_create: GroupCreate) -> Group:
    '''Создать группу'''
    group = Group(**group_create.model_dump())
    db.add(group)
    await db.commit()
    await db.refresh(group)
    return group

async def update_student(db: AsyncSession, student_id: int, updates: dict) -> Student | None:
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        return None
    for key, value in updates.items():
        setattr(student, key, value)
    await db.commit()
    await db.refresh(student)
    return student