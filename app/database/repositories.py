from typing import Generic, TypeVar
from collections.abc import Sequence

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.types import ModelType, SchemaType

RepoType = TypeVar('RepoType', bound='BaseRepository')

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
        self.pk_column = self.model.__mapper__.primary_key[0]

    async def create(self, schema: SchemaType) -> ModelType:
        model_obj = self.model(**schema.model_dump())

        self.session.add(model_obj)
        await self.session.commit()
        await self.session.refresh(model_obj)

        return model_obj

    async def get_by_id(self, id: int | str) -> ModelType | None:
        stmt = select(self.model).where(self.pk_column == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> Sequence[ModelType]:
        """
        Получить все записи этой модели.
        """
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_by_id(self, id: int | str) -> bool:
        """
        Удалить запись по ID. Вернёт True, если запись была удалена.
        """
        stmt = delete(self.model).where(self.pk_column == id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def update_by_id(self, id: int, schema: SchemaType) -> bool:
        data = schema.model_dump(exclude_unset=True)

        if not data:
            return False

        stmt = (
            update(self.model)
            .where(self.pk_column == id)
            .values(**data)
            .execution_options(synchronize_session="fetch")  # Важно для синхронизации с сессией
        )

        result = await self.session.execute(stmt)
        await self.session.commit()

        return result.rowcount > 0

    async def exists(self, id: int | str) -> bool:
        """
        Проверка: существует ли запись с таким ID.
        """
        return await self.get_by_id(id) is not None

