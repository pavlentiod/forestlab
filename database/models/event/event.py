from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, Boolean, func, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base

if TYPE_CHECKING:
    from src.database.models.track.track import Track


class Event(Base):
    title: Mapped[str] = mapped_column(String(100), nullable=False, server_default="EventTitle", default="EventTitle")
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False)
    splits: Mapped[str] = mapped_column(JSONB, nullable=False, server_default="{}", default="{}")
    courses: Mapped[str] = mapped_column(JSONB, nullable=False, server_default="{}", default="{}")
    results: Mapped[str] = mapped_column(JSONB, nullable=False, server_default="{}", default="{}")
    groups: Mapped[str] = mapped_column(JSONB, nullable=False, server_default="{}", default="{}")
    runners: Mapped[str] = mapped_column(JSONB, nullable=False, server_default="{}", default="{}")
    legs: Mapped[str] = mapped_column(JSONB, nullable=False, server_default="{}", default="{}")
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), server_default=func.now())

    tracks: Mapped[list["Track"]] = relationship(back_populates="event_rel")
