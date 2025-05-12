from app.orders.repositories import OrderRepository
from app.services import BaseService

class OrderService(BaseService[OrderRepository]):
    def __init__(self, order_repository: OrderRepository):
        super().__init__(order_repository)
        self.order_repository = order_repository
