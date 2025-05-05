from sqlalchemy.orm import Mapped, mapped_column

from app.database.engine import Base
from sqlalchemy import String, Boolean, DateTime
import datetime


def generate_registration_code():
    return '1234'


def generate_auth_token():
    return 'token1234'


class Device(Base):
    __tablename__ = 'devices'
    name: Mapped[str] = mapped_column(String, nullable=False)
    registration_code: Mapped[str] = mapped_column(String, unique=True, default=generate_registration_code)
    auth_token: Mapped[str] = mapped_column(String, unique=True, default=generate_auth_token)
    is_registered: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=None)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=None)
