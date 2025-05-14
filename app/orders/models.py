from sqlalchemy import Time, Date, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.engine import Base
import datetime


class OrderInfo(Base):
    __tablename__ = 'order_info'
    id: Mapped[int] = mapped_column(primary_key=True)
    payment_name: Mapped[str] = mapped_column(nullable=True)
    device_id: Mapped[int] = mapped_column(ForeignKey('device.id'), nullable=True)
    transaction_id: Mapped[str] = mapped_column(nullable=True)
    amount: Mapped[float] = mapped_column(nullable=True)
    date = mapped_column(Date, nullable=True)
    time = mapped_column(Time, nullable=True)
    status: Mapped[bool] = mapped_column(nullable=True)
    log: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now)
