from datetime import datetime

from fastapi import APIRouter

from app.classes.dao import (
    CRUDClass,
    CRUDClassGrammar,
    CRUDClassTopic,
    CRUDClassUserLesson,
    CRUDClassWord,
)
from app.contents.dao import CRUDGrammar, CRUDTopic, CRUDUsefulLink, CRUDWord
from app.contents.models import Grammar, Topic, UsefulLink, Word
from app.contents.schemas import (
    GrammarCreateSchema,
    GrammarGetSchema,
    TopicCreateSchema,
    TopicGetSchema,
    UsefulLinkCreateSchema,
    UsefulLinkGetSchema,
    WordCreateKanaTranslSchema,
    WordCreateSchema,
    WordGetSchema,
)
from app.database import SessionDep
from app.exceptions import ObjectAlreadyExistsException
from app.users.models import User
from app.users.schemas import UserGetSchema
from app.users.services import CurrentUserDep

router = APIRouter(
    prefix="/contents",
    tags=["Материал"],
)

# TODO: add a word to the class: check at words, add to class words, if present in words update there
# TODO: get words for for the class
# TODO: get all words of user
# TODO: get all words of a lesson
# TODO: get words for the user in the last 3 classes
# TODO: get words for the user in between two dates


# @router.post("/add_word")
# async def add_word(
#     session: SessionDep,
#     word_data: WordCreateSchema,
# ):

#     new_class = await CRUDWord.check_add(
#         session,
#         **class_data,
#     )
#     return {"msg": f"Class {new_class} created."}


@router.get("/popup_word")
async def popup_word(
    session: SessionDep,
    word_data: WordCreateKanaTranslSchema,
) -> WordGetSchema:
    word = await CRUDWord.search_word(
        session=session,
        kana=word_data.kana,
        translation=word_data.translation,
    )
    return word


@router.get("/get_word")
async def get_word(
    session: SessionDep,
    kana: str,
    translation: str,
) -> WordGetSchema:
    word = await CRUDWord.get_one_or_none(
        session=session,
        kana=kana,
        translation=translation,
    )
    return word


# async def get_class_words(
#     session: SessionDep,
#     user: CurrentUserDep,
# ) -> list[ClassGetSchema]:
#     classes = await CRUDClass.get_classes(
#         session=session,
#         user_id=user.id,
#     )
#     return classes
