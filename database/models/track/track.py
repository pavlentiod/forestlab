from uuid import UUID as uuid_1

from sqlalchemy import Float, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.models.event.event import Event


class Track(Base):
    runner: Mapped[uuid_1] = mapped_column(UUID(as_uuid=True), nullable=False)
    distance: Mapped[float] = mapped_column(Float, nullable=False)
    elevation: Mapped[float] = mapped_column(Float, nullable=False)
    duration: Mapped[float] = mapped_column(Float, nullable=False)
    points: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default="{}")

    event: Mapped[uuid_1] = mapped_column(ForeignKey("events.id"), nullable=False)
    event_rel: Mapped["Event"] = relationship(back_populates="tracks")