import re
from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator

from app.classes.models import EntityType
from app.textbooks.schemas import UserLessonGetSchema


class WordCreateKanaTranslSchema(BaseModel):
    kana: str = Field(example="ひらがな or カタカナ")
    translation: Optional[str] = Field(None, example="перевод")

    @field_validator("kana")
    @classmethod
    def check_kana(cls, value: str) -> str:
        if not re.fullmatch(r"^[\u3040-\u309F\u30A0-\u30FF\s]+$", value):
            raise ValueError("Should only contain hiragana or katakana characters")
        return value


class WordBaseSchema(BaseModel):
    kanji: Optional[str] = Field(None, example="漢字")
    kana: str = Field(example="ひらがな or カタカナ")
    translation: Optional[str] = Field(None, example="перевод")
    example_sentences: Optional[str] = Field(None, example="これは例文です。")

    @field_validator("kana")
    @classmethod
    def check_kana(cls, value: str) -> str:
        if not re.fullmatch(r"^[\u3040-\u309F\u30A0-\u30FF\s]+$", value):
            raise ValueError("Should only contain hiragana or katakana characters")
        return value

    @field_validator("kanji")
    @classmethod
    def check_if_any_kanji(cls, value):
        if value is None:
            return value
        if not re.search(r"[\u4E00-\u9FAF]+", value):
            raise ValueError("Should contain at least one kanji character")
        return value


class WordCreateSchema(WordBaseSchema):
    lesson_id: int | None = Field(None)


class WordGetSchema(WordCreateSchema):
    id: int = Field(gt=0)


class UsefulLinkCreateSchema(BaseModel):
    url: HttpUrl
    description: str
    entity_type: EntityType
    grammar_id: Optional[int] = Field(None, gt=0)
    topic_id: Optional[int] = Field(None, gt=0)

    @model_validator(mode="after")
    def check_entity_type(self):
        if self.entity_type == EntityType.GRAMMAR:
            if self.topic_id:
                raise ValueError("topic_id must be None")
            elif self.grammar_id is None:
                raise ValueError("grammar_id must be set")
        elif self.entity_type == EntityType.TOPIC:
            if self.grammar_id:
                raise ValueError("grammar_id must be None")
            elif self.topic_id is None:
                raise ValueError("topic_id must be set")
        return self


class UsefulLinkGetSchema(UsefulLinkCreateSchema):
    id: int = Field(gt=0)


class GrammarCreateSchema(BaseModel):
    name_russian: str = Field(..., example="Грамматика")
    name_japanese: Optional[str] = Field(None, example="文法")
    lesson_id: int


class GrammarGetSchema(GrammarCreateSchema):
    id: int = Field(gt=0)


class TopicCreateSchema(BaseModel):
    name_russian: str = Field(..., example="Грамматика")
    name_japanese: Optional[str] = Field(None, example="文法")
    lesson_id: int


class TopicGetSchema(TopicCreateSchema):
    id: int = Field(gt=0)
