from typing import TypeVar

from pydantic import BaseModel

from app.database.engine import Base

ModelType = TypeVar('ModelType', bound=Base)
SchemaType = TypeVar('SchemaType', bound=BaseModel)
