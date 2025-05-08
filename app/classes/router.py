from datetime import datetime

from fastapi import APIRouter

from app.classes.dao import (
    CRUDClass,
    CRUDClassGrammar,
    CRUDClassTopic,
    CRUDClassUserLesson,
    CRUDClassWord,
)
from app.classes.models import (
    Class,
    ClassGrammar,
    ClassTopic,
    ClassUserLesson,
    ClassWord,
)
from app.classes.schemas import (
    ClassBaseSchema,
    ClassCreateSchema,
    ClassGetSchema,
    ClassSimpleGetSchema,
)
from app.contents.dao import CRUDGrammar, CRUDTopic, CRUDUsefulLink, CRUDWord
from app.contents.router import router as contents_router
from app.database import SessionDep
from app.exceptions import ObjectAlreadyExistsException
from app.users.models import User
from app.users.schemas import UserGetSchema
from app.users.services import CurrentUserDep

router = APIRouter(
    prefix="/classes",
    tags=["Уроки"],
)


@router.get("/")
async def get_user_classes(
    session: SessionDep,
    user: CurrentUserDep,
) -> list[ClassGetSchema]:
    classes = await CRUDClass.get_classes(
        session=session,
        user_id=user.id,
    )
    return classes


@router.get("/{class_id}")
async def get_class(
    session: SessionDep,
    class_id: int,
) -> ClassSimpleGetSchema:
    class_selected = await CRUDClass.get_class_simple(
        session=session,
        class_id=class_id,
    )
    return class_selected


@router.post("/add_class")
async def add_user_class(
    session: SessionDep,
    user: CurrentUserDep,
    class_data: ClassBaseSchema,
):
    class_data = class_data.model_dump()
    class_data["user_id"] = user.id
    class_data["slug"] = None
    new_class = await CRUDClass.check_add(
        session,
        **class_data,
    )
    return {"msg": f"Class {new_class} created."}
