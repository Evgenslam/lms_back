from pydantic import BaseModel, EmailStr


class TextbookCreateSchema(BaseModel):
    name: str
    slug: str


class TextbookGetSchema(BaseModel):
    id: int
    name: str
    completed: bool


class LessonCreateSchema(BaseModel):
    name: str
    slug: str
    textbook_id: int


class LessonGetSchema(BaseModel):
    id: int
    name: str
    slug: str


class UserTextbookCreateSchema(BaseModel):
    user_id: int
    textbook_id: int


class UserTextbookGetSchema(BaseModel):
    id: int
    user_id: int
    textbook_id: int


class UserLessonCreateSchema(BaseModel):
    user_id: int
    lesson_id: int
    usertextbook_id: int


class UserLessonGetSchema(BaseModel):
    id: int
    user_id: int
    lesson_id: int
    usertextbook_id: int
