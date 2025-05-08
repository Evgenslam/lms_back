from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.exceptions import IncorrectEmailOrPasswordException
from app.users.dao import CRUDUser

algo = settings.ALGORITHM
secret = settings.SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# TODO: user better hashing (https://stepik.org/lesson/919993/step/5?unit=925776)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=240)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=secret, algorithm=algo)
    return encoded_jwt


async def authenticate_user(session: AsyncSession, email: EmailStr, password: str):
    user = await CRUDUser.get_one_or_none(
        session=session,
        email=email,
    )
    if not (user and verify_password(password, user.hashed_password)):
        raise IncorrectEmailOrPasswordException
    return user
