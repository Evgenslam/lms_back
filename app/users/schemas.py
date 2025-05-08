from pydantic import BaseModel, EmailStr


class UserIdGetSchema(BaseModel):
    id: int


class UserGetSchema(UserIdGetSchema):
    name: str
    slug: str
    email: EmailStr


class UserCreateSchema(BaseModel):
    name: str
    slug: str
    email: EmailStr
    password: str


class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str
