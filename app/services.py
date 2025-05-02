from collections.abc import Sequence
from typing import Generic

from app.database.repositories import RepoType
from app.types import SchemaType, ModelType


class BaseService(Generic[RepoType]):
    def __init__(self, db_repository: type[RepoType]):
        self.db_repository = db_repository

    async def create(self, schema: SchemaType) -> ModelType | None:
        return await self.db_repository.create(schema)

    async def get_by_id(self, id) -> ModelType | None:
        return await self.db_repository.get_by_id(id)

    async def list_all(self) -> Sequence[ModelType]:
        return await self.db_repository.list_all()

    async def delete_by_id(self, id) -> bool:
        return await self.db_repository.delete_by_id(id)

    async def update_by_id(self, id, schema: SchemaType) -> bool:
        return await self.db_repository.update_by_id(id, schema)
