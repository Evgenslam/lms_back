from typing import Annotated

from fastapi import Depends
from sqlalchemy import TIMESTAMP, Integer, MetaData, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.config import settings

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True,
)

"""The newer easier way to create async session generator"""
new_session = async_sessionmaker(engine, expire_on_commit=False)


# TODO: type hints like in https://www.youtube.com/watch?v=XWJWJfTWjSs&t=3811s
async def get_session() -> AsyncSession:
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):

    metadata = MetaData(
        naming_convention=settings.NAME_CONVENTION,
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
    )
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
    )
