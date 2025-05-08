from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from fastapi import HTTPException
from slugify import slugify
from sqlalchemy import and_, delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from unidecode import unidecode

from app.config import settings
from app.exceptions import ObjectAlreadyExistsException


class CRUDBase:

    model = None

    @classmethod
    async def get_by_id(
        cls,
        session: AsyncSession,
        model_id: int,
    ):
        query = select(cls.model).filter_by(id=model_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_one_or_none(
        cls,
        session: AsyncSession,
        **filters: dict,
    ):
        query = select(cls.model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
        **filters,
    ):
        query = select(cls.model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_all_by_feature(
        cls,
        session: AsyncSession,
        feature: str,
        feature_list: list,
    ):
        column = getattr(cls.model, feature)
        query = select(cls.model).filter(column.in_(feature_list))
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    def slugify_if_needed(
        cls,
        data: dict,
    ):
        attr_to_slugify = settings.SLUGIFY_ATTR_BY_MODEL[cls.model.__name__]
        if not data["slug"]:
            data["slug"] = slugify(unidecode(data[attr_to_slugify]), allow_unicode=True)

    # TODO: use HTTPException instead of ValueError
    @classmethod
    async def add(
        cls,
        session: AsyncSession,
        **data,
    ):
        new_obj = cls.model(**data)
        session.add(new_obj)
        try:
            await session.commit()
            await session.refresh(new_obj)
            return new_obj
        except IntegrityError as e:
            await session.rollback()
            error_message = str(e.orig)
            if "UniqueViolationError" in error_message:
                existing_object = settings.EXCEPTION_TEXT_BY_MODEL.get(
                    cls.model.__name__, "Object"
                )
                print(existing_object)
                raise ObjectAlreadyExistsException(existing_object)
            elif "ForeignKeyViolationError" in error_message:
                raise ValueError("Объект ссылается на несуществующую запись")
            else:
                raise ValueError("Ошибка целостности данных.")

    @classmethod
    async def check_add(
        cls,
        session: AsyncSession,
        **data: dict,
    ):
        data = data.copy()
        cls.slugify_if_needed(data)
        return await cls.add(session, **data)

    @classmethod
    async def add_bulk(
        cls,
        session: AsyncSession,
        data: list[dict],
    ):
        objects = [cls.model(**obj) for obj in data]
        session.add_all(objects)
        await session.commit()
        return objects

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        filters: dict,
        **data,
    ):
        stmt = update(cls.model).filter_by(**filters).values(**data)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def delete(
        cls,
        session: AsyncSession,
        **filters,
    ):
        stmt = select(cls.model).filter_by(**filters)
        result = await session.execute(stmt)
        obj = result.scalars().one_or_none()

        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")

        await session.delete(obj)
        await session.commit()

    @classmethod
    async def delete_bulk(
        cls,
        session: AsyncSession,
        filters: dict[str, list],
    ):
        conditions = [
            getattr(cls.model, column).in_(values) for column, values in filters.items()
        ]
        stmt = delete(cls.model).where(and_(*conditions))
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount
