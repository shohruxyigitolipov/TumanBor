from sqlalchemy.orm import Mapped, mapped_column

from app.database.engine import Base
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Date, Time
import datetime
from sqlalchemy.orm import relationship


def generate_registration_code():
    return '1234'


def generate_auth_token():
    return 'abc1234'


class Device(Base):
    __tablename__ = 'device'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=None, nullable=True)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=None, nullable=True)
    data: Mapped["DeviceDatas"] = relationship('DeviceDatas', back_populates='device', uselist=False,
                                               cascade='all, delete')


class DeviceDatas(Base):
    __tablename__ = 'device_data'
    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("device.id"), unique=True)
    registration_code: Mapped[str] = mapped_column(String, unique=True, default=generate_registration_code)
    auth_token: Mapped[str] = mapped_column(String, unique=True, default=generate_auth_token)
    device: Mapped["Device"] = relationship("Device", back_populates="data")

