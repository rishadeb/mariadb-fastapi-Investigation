from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime


class Base(DeclarativeBase):
    pass


class KatcpSensor(Base):
    __tablename__ = "katcpsensor"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime)
    device: Mapped[str] = mapped_column(String(8))
    name: Mapped[str] = mapped_column(String(32))
    status: Mapped[int]
    value: Mapped[str] = mapped_column(String(20))

    def __repr__(self) -> str:
        return (
            f"KatcpSensor(id={self.id!r}, timestamp={self.timestamp!r}, device={self.device!r},"
            f"name={self.name!r}, status={self.status!r}, value={self.value!r})"
        )


class KatcpComms(Base):
    __tablename__ = "katcpcomms"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime)
    device: Mapped[str] = mapped_column(String(8))
    message: Mapped[str] = mapped_column(String(1024))

    def __repr__(self) -> str:
        return (
            f"KatcpComms(id={self.id!r}, timestamp={self.timestamp!r}, device={self.device!r})"
            f"message={self.message!r}"
        )


class KatcpLogs(Base):
    __tablename__ = "katcplogs"

    id: Mapped[int] = mapped_column(primary_key=True)
    device: Mapped[str] = mapped_column(String(8))
    level: Mapped[int]
    timestamp: Mapped[datetime] = mapped_column(DateTime)
    name: Mapped[str] = mapped_column(String(64))
    message: Mapped[str] = mapped_column(String(1024))

    def __repr__(self) -> str:
        return (
            f"KatcpLogs(id={self.id!r}, timestamp={self.timestamp!r}, device={self.device!r}"
            f"name={self.name!r}, level={self.level!r}, message={self.message!r})"
        )
