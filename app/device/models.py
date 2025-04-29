from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Device(Base):
    __tablename__ = 'devices'
    device_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()
