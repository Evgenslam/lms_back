from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.classes.models import (
    Class,
    ClassGrammar,
    ClassTopic,
    ClassUserLesson,
    ClassWord,
)
from app.services import CRUDBase


class CRUDClass(CRUDBase):

    model = Class

    @classmethod
    async def get_class_simple(cls, session: AsyncSession, class_id: int):
        query = (
            select(cls.model)
            .options(joinedload(cls.model.user))
            .options(selectinload(cls.model.words))
            .where(cls.model.id == class_id)
        )
        res = await session.execute(query)
        return res.scalar_one_or_none()

    @classmethod
    async def get_classes(cls, session: AsyncSession, user_id: int):
        query = (
            select(cls.model)
            .options(selectinload(cls.model.userlessons))
            .options(selectinload(cls.model.words))
            .options(selectinload(cls.model.grammar_topics))
            .options(selectinload(cls.model.other_topics))
            .where(cls.model.user_id == user_id)
        )
        res = await session.execute(query)
        return res.scalars().all()


class CRUDClassWord(CRUDBase):

    model = ClassWord


class CRUDClassGrammar(CRUDBase):

    model = ClassGrammar


class CRUDClassTopic(CRUDBase):

    model = ClassTopic


class CRUDClassUserLesson(CRUDBase):

    model = ClassUserLesson
