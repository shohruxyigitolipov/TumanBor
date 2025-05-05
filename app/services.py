from collections.abc import Sequence
from typing import Generic

from app.database.repositories import RepoType
from app.obj_types import SchemaType, ModelType


class BaseService(Generic[RepoType]):
    def __init__(self, repo: type[RepoType]):
        self.repo = repo

    async def create(self, schema: SchemaType) -> ModelType | None:
        return await self.repo.create(schema)

    async def get_by_id(self, id) -> ModelType | None:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> Sequence[ModelType]:
        return await self.repo.list_all()

    async def delete_by_id(self, id) -> bool:
        return await self.repo.delete_by_id(id)

    async def update_by_id(self, id, schema: SchemaType) -> bool:
        return await self.repo.update_by_id(id, schema)
