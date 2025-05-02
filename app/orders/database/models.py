from sqlalchemy import Time, Date, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.engine import Base


class Order(Base):
    __tablename__ = 'orders'

    payment_name: Mapped[str] = mapped_column(nullable=True)
    device_id: Mapped[int] = mapped_column(ForeignKey('devices.device_id'), nullable=True)
    transaction_id: Mapped[str] = mapped_column(nullable=True)
    amount: Mapped[float] = mapped_column(nullable=True)
    date = mapped_column(Date, nullable=True)
    time = mapped_column(Time, nullable=True)
    status: Mapped[bool] = mapped_column(nullable=True)
    log: Mapped[str] = mapped_column(nullable=True)
    finished: Mapped[bool] = mapped_column(default=False)
    created_at = mapped_column(DateTime, default=func.now())
