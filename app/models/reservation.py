from sqlalchemy import String, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import uuid


class Reservation(Base):
    __tablename__ = 'reservations'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    reservation_code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    room_id: Mapped[str] = mapped_column(String, ForeignKey('rooms.id'))
    location_id: Mapped[str] = mapped_column(String, ForeignKey('locations.id'))
    user_id: Mapped[str] = mapped_column(String, ForeignKey('users.id'))
    date_ranges: Mapped[list] = mapped_column(JSON)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    modified_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    room = relationship("Room")
    location = relationship("Location")
    user = relationship("User")
