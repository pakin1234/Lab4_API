from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__ = "student"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    middlename: Mapped[str] = mapped_column(String(30), nullable=True)
    age: Mapped[int] = mapped_column(Integer)
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id", ondelete="SET NULL"), nullable=True)

    group: Mapped["Group"] = relationship(back_populates="students")

class Group(Base):
    __tablename__ = "group"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_number: Mapped[str] = mapped_column(String(10))

    students: Mapped[list["Student"]] = relationship(back_populates="group", cascade="all, delete-orphan")