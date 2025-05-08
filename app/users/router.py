from fastapi import APIRouter, Depends, Response
from slugify import slugify
from unidecode import unidecode

from app.classes.dao import CRUDClass
from app.classes.router import router as classes_router
from app.classes.schemas import ClassGetSchema
from app.database import SessionDep
from app.exceptions import EmailAlreadyExistsException
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import CRUDUser
from app.users.schemas import (
    UserAuthSchema,
    UserCreateSchema,
    UserGetSchema,
    UserIdGetSchema,
)
from app.users.services import CurrentUserDep, check_user_exists, slugify_username

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)

router.include_router(classes_router, prefix="/{user_id}")


@router.post("/register")
async def register_user(
    session: SessionDep,
    user_data: UserCreateSchema,
):
    user = await CRUDUser.check_add(
        session=session,
        name=user_data.name,
        slug=user_data.slug,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
    )
    return {"msg": f"Создан {user}."}


@router.post("/login")
async def login_user(
    session: SessionDep,
    response: Response,
    user_data: UserAuthSchema,
):
    user = await authenticate_user(
        session,
        user_data.email,
        user_data.password,
    )
    token = create_access_token({"sub": str(user.id)})
    response.set_cookie(
        "user_access_token",
        token,
        httponly=True,
        samesite="lax",
    )
    return {"access_token": token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("user_access_token")
    return {"msg": f"User logged out."}


@router.get("/me")
async def get_current_user(
    user: CurrentUserDep,
) -> UserIdGetSchema:
    return user


@router.get("")
async def get_users(session: SessionDep) -> list[UserGetSchema]:
    result = await CRUDUser.get_all(session)
    return result


@router.get("/{user_id}")
async def get_user_by_id(
    session: SessionDep,
    user_id: int,
) -> UserGetSchema | None:
    return await CRUDUser.get_by_id(session, user_id)


@router.delete("/{user_name}")
async def delete_user(
    session: SessionDep,
    user_name: str,
):
    await CRUDUser.delete(session=session, name=user_name)
    return {"msg": "User deleted."}


@router.delete("/")
async def bulk_delete_users(
    session: SessionDep,
    filters: dict[str, list],
):
    result = await CRUDUser.delete_bulk(
        session=session,
        filters=filters,
    )
    return {"msg": f"{result} users deleted."}
