from sqlalchemy.ext.asyncio import AsyncSession

from app.orders.models import Order
from app.database.repositories import BaseRepository

class OrderRepository(BaseRepository[Order]):
    def __init__(self, session: AsyncSession):
        super().__init__(Order, session)
