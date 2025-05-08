from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.contents.models import Grammar, Topic, UsefulLink, Word
from app.contents.schemas import WordCreateKanaTranslSchema, WordGetSchema
from app.services import CRUDBase


class CRUDWord(CRUDBase):

    model = Word

    @classmethod
    async def search_word(
        cls,
        session: AsyncSession,
        kana: str,
        translation: str,
    ):
        query = (
            select(cls.model)
            .where(cls.model.kana == kana)
            .filter(cls.model.translation.contains(translation.lower()))
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def add_word(
        cls, session: AsyncSession, word_data: WordCreateKanaTranslSchema
    ) -> WordGetSchema | str:
        word = await cls.search_word(
            session=session,
            kana=word_data.kana,
            translation=word_data.translation,
        )
        """
        If the word is there, we return it
        """
        if word:
            return word
        # If the word is not there, we save it on blur to display to the student


class CRUDGrammar(CRUDBase):

    model = Grammar


class CRUDTopic(CRUDBase):

    model = Topic


class CRUDUsefulLink(CRUDBase):

    model = UsefulLink
