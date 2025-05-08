from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from jose import ExpiredSignatureError, JWTError, jwt
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession
from unidecode import unidecode

from app.config import settings
from app.database import SessionDep
from app.exceptions import (
    EmailAlreadyExistsException,
    IncorrectTokenFormatException,
    TokenExpiredException,
    UserNotFoundException,
)
from app.users.dao import CRUDUser
from app.users.schemas import UserCreateSchema, UserGetSchema


async def check_user_exists(
    session: AsyncSession,
    user_data: UserCreateSchema,
) -> None:
    existing_user = await CRUDUser.get_one_or_none(
        session=session,
        email=user_data.email,
    )
    if existing_user:
        raise EmailAlreadyExistsException


def slugify_username(user_data: UserCreateSchema) -> str:
    if not user_data.slug:
        return slugify(unidecode(user_data.name), allow_unicode=True)
    return user_data.slug


def get_token(request: Request):
    token = request.cookies.get("user_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return token


async def get_current_user(
    session: SessionDep,
    token: str = Depends(get_token),
):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALGORITHM,
        )
    except JWTError:
        raise IncorrectTokenFormatException
    except ExpiredSignatureError:
        raise TokenExpiredException
    user_id = payload.get("sub")
    if not user_id:
        raise UserNotFoundException
    user = await CRUDUser.get_by_id(
        session,
        int(user_id),
    )
    if not user:
        raise UserNotFoundException
    return user


CurrentUserDep = Annotated[UserGetSchema, Depends(get_current_user)]
