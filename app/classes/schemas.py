import re
from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator

from app.classes.models import EntityType
from app.contents.schemas import GrammarGetSchema, TopicGetSchema, WordGetSchema
from app.textbooks.schemas import UserLessonGetSchema


class ClassBaseSchema(BaseModel):
    class_date: date
    name: str


class ClassCreateSchema(BaseModel):
    pass


class ClassSimpleGetSchema(ClassBaseSchema):
    id: int = Field(gt=0)
    words: Optional[list[WordGetSchema]] = None


class ClassGetSchema(ClassBaseSchema):
    id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    slug: Optional[str] = None
    plan: Optional[str] = None
    homework: Optional[str] = None
    questions: Optional[str] = None
    userlessons: Optional[list[UserLessonGetSchema]] = None
    words: Optional[list[WordGetSchema]] = None
    grammar_topics: Optional[list[GrammarGetSchema]] = None
    other_topics: Optional[list[TopicGetSchema]] = None
