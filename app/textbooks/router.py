from fastapi import APIRouter, Depends
from slugify import slugify
from sqlalchemy import select, text
from unidecode import unidecode

from app.database import SessionDep
from app.textbooks.dao import CRUDLesson, CRUDTextbook, CRUDUserLesson, CRUDUserTextbook
from app.textbooks.models import Lesson, Textbook, UserLesson, UserTextbook
from app.textbooks.schemas import (
    LessonCreateSchema,
    TextbookCreateSchema,
    TextbookGetSchema,
    UserTextbookCreateSchema,
)
from app.users.schemas import UserGetSchema
from app.users.services import CurrentUserDep

router = APIRouter(
    prefix="/textbooks",
    tags=["Учебники"],
)


@router.post("/create_textbook")
async def create_textbook(
    session: SessionDep,
    textbook_data: TextbookCreateSchema,
):
    textbook = await CRUDTextbook.check_add(
        session=session,
        name=textbook_data.name,
        slug=textbook_data.slug,
    )
    return {"msg": f"Textbook {textbook} created."}


@router.post("/create_lesson")
async def create_lesson(
    session: SessionDep,
    lesson_data: LessonCreateSchema,
):
    lesson = await CRUDLesson.check_add(
        session=session,
        data=lesson_data.model_dump(),
    )
    return {"msg": f"Lesson {lesson} created."}


# TODO: refactor bulk actions
# TODO: rethink the DOM
@router.post("/create_many_lessons")
async def create_lessons(
    session: SessionDep,
    lessons_data: list[LessonCreateSchema],
):
    names = [x.name for x in lessons_data]
    existing_lessons = await CRUDLesson.get_all_by_feature(
        session=session,
        feature="name",
        feature_list=names,
    )
    if existing_lessons:
        raise Exception(f"Lessons {existing_lessons} already exist.")
    for lesson_data in lessons_data:
        if not lesson_data.slug:
            lesson_data.slug = slugify(unidecode(lesson_data.name), allow_unicode=True)
    lessons = await CRUDLesson.add_bulk(
        session,
        [dict(x) for x in lessons_data],
    )
    return {
        "msg": f"Next lessons created: "
        f"{', '.join([lesson.name for lesson in lessons])}"
    }


@router.post("/add_textbook_for_user")
async def add_textbook_for_user(
    session: SessionDep,
    data: UserTextbookCreateSchema,
):
    usertextbook = await CRUDUserTextbook.add(
        session=session,
        user_id=data.user_id,
        textbook_id=data.textbook_id,
    )
    usertextbook_id = usertextbook.id
    lessons = await CRUDLesson.get_all(
        session=session,
        textbook_id=usertextbook.textbook_id,
    )
    lessons_ids = [lesson.id for lesson in lessons]
    userlessons = [
        {
            "user_id": data.user_id,
            "lesson_id": lesson_id,
            "usertextbook_id": usertextbook_id,
        }
        for lesson_id in lessons_ids
    ]
    await CRUDUserLesson.add_bulk(session, userlessons)
    return {
        "msg": f"Textbook {usertextbook.textbook_id} added for user {usertextbook.user_id}."
    }


@router.get("/all")
async def get_all(session: SessionDep) -> list[TextbookGetSchema]:
    return await CRUDTextbook.get_all(session)


@router.post("/update_lesson_status")
async def update_lesson_status(
    session: SessionDep,
    userlesson_id: int,
    completed: bool,
):
    await CRUDUserLesson.update(
        session=session,
        filters={"id": userlesson_id},
        completed=completed,
    )
    return f"msg: Lesson {userlesson_id} completion status updated to {completed}."


@router.get("/")
async def get_user_lessons(
    session: SessionDep,
    user: CurrentUserDep,
):
    ut_query = text(
        """
        select t.id, t.name, ut.completed
        from usertextbook ut
        join textbook t on t.id = ut.textbook_id
        where ut.user_id = :user_id
        """
    )
    res = await session.execute(ut_query, {"user_id": user.id})
    usertextbooks = res.mappings().all()
    usertextbooks = [dict(ut) for ut in usertextbooks]

    for i, ut in enumerate(usertextbooks):
        ul_query = text(
            """
            select ul.id, l.name, ul.completed
            from userlesson ul
            join lesson l on l.id = ul.lesson_id
            where ul.user_id = :user_id and ul.lesson_id in (select id from lesson l where l.textbook_id = :textbook_id)
            """
        )
        res = await session.execute(
            ul_query, {"user_id": user.id, "textbook_id": ut["id"]}
        )
        lessons = [dict(row) for row in res.mappings().all()]
        usertextbooks[i]["lessons"] = lessons

    return usertextbooks

    # query = (
    #     select(UserTextbook)
    #     .options(joinedload(UserTextbook.textbook).load_only(Textbook.name))
    #     .options(
    #         selectinload(UserTextbook.userlessons)
    #         .joinedload(UserLesson.lesson)
    #         .load_only(Lesson.name)
    #     )
    #     .where(User.id == user.id)
    # )
    # res = await session.execute(query)
    # res = res.scalars().all()
    # return res

    # query = (
    #     select(UserTextbook)
    #     .join(UserTextbook.textbook)
    #     .options(contains_eager(UserTextbook.textbook))
    #     .where(User.id == user.id)
    # )
    # res = await session.execute(query)
    # return res.scalars().all()

    # Как вывести данные селектами

    # query = (
    #     select(
    #         UserTextbook.user_id,
    #         UserTextbook.completed,
    #         Textbook.name,
    #         Textbook.id,
    #     )
    #     .join(Textbook)
    #     .where(UserTextbook.user_id == user.id)
    # )
    # res = await session.execute(query)
    # res = res.all()
    # for r in res:
    #     printie = r
    #     query_l = (
    #         select(Lesson.name, UserLesson.completed)
    #         .join(Lesson, UserLesson.lesson_id == Lesson.id)
    #         .filter(
    #             UserLesson.user_id == printie[0],
    #             Lesson.textbook_id == printie[3],
    #         )
    #     )
    #     lessons = await session.execute(query_l)
    #     print(printie)
    #     for l in lessons:
    #         print(l)
    # r.append({"lessons": lessons})

    # query_l = (
    #     select()
    # )

    # return res
    # query = (
    #     select(UserTextbook)
    #     .options(
    #         joinedload(UserTextbook.textbook)
    #         .selectinload(Textbook.lessons)
    #         .joinedload(Lesson.users)
    #     )
    #     .where(UserTextbook.user_id == user.id)
    # )
    # res = await session.execute(query)
    # res = res.scalars().all()
    # return res
    # return [
    #     {
    #         "name": r.textbook.name,
    #         "completed": r.completed,
    #         "lessons": r.textbook.lessons,
    #     }
    #     for r in res
    # ]
    # Как вывести только нужные колонки
    # query = (
    #     select(ut.completed, t.name)
    #     .join(t, ut.textbook_id == t.id)
    #     .where(ut.user_id == user.id)
    # )

    # res = await session.execute(query)
    # return res.mappings().all()
    # return [{"name": r[0], "completed": r[1].completed} for r in res]

    # user_id = user.id
    # return await CRUDLesson.get_all(id=user_id)


# @router.post("/")
# async def create_user(user_data: UserDTO):
#     existing_user = await CRUDUser.get_one_or_none(name=user_data.name)
#     if existing_user:
#         raise NameAlreadyExistsException
#     if not user_data.slug:
#         user_data.slug = slugify(unidecode(user_data.name), allow_unicode=True)
#     user = await CRUDUser.add(name=user_data.name, slug=user_data.slug)
#     return {"msg": f"User {user} created."}


# @router.delete("/{user_name}")
# async def delete_user(user_name: str):
#     await CRUDUser.delete(name=user_name)
#     return {"msg": "User deleted."}


# @router.delete("/")
# async def bulk_delete_users(filters: dict[str, list]):
#     result = await CRUDUser.delete_bulk(filters)
#     return {"msg": f"{result} users deleted."}
