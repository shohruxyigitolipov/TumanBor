from sqlalchemy.ext.asyncio import AsyncSession

from app.orders.models import OrderInfo
from app.database.repositories import BaseRepository

class OrderRepository(BaseRepository[OrderInfo]):
    def __init__(self, session: AsyncSession):
        super().__init__(OrderInfo, session)
