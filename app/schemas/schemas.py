from pydantic import BaseModel, ConfigDict, Field

class GroupBase(BaseModel):
    group_number: str = Field(..., min_length=1, max_length=100, description="Номер группы")

    model_config = ConfigDict(from_attributes=True)

class GroupCreate(GroupBase):
    pass

class GroupResponse(GroupBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class GroupWithStudents(GroupResponse):
    students: list["StudentResponse"] = []

    model_config = ConfigDict(from_attributes=True)

class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Имя студента")
    surname: str = Field(..., min_length=1, max_length=100, description="Фамилия студента")
    middlename: str | None = Field(None, max_length=100, description="Отчество студента")
    age: int = Field(..., ge=16, le=80)

    model_config = ConfigDict(from_attributes=True)

class StudentCreate(StudentBase):
    group_id: int | None = Field(None, description="ID группы")

class StudentUpdate(StudentBase):
    name: str | None = Field(None, min_length=1, max_length=100, description="Имя студента")
    surname: str | None = Field(None, min_length=1, max_length=100, description="Фамилия студента")
    middlename: str | None = Field(None, max_length=100, description="Отчество студента")
    age: int | None = Field(None, ge=16, le=80)
    group_id: int | None = Field(None, description="ID группы")

class StudentResponse(StudentBase):
    id: int
    group_id: int | None

    model_config = ConfigDict(from_attributes=True)

