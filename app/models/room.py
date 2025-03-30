from sqlalchemy import String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.database import Base
import uuid


class Room(Base):
    __tablename__ = 'rooms'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    room_number: Mapped[int] = mapped_column(String(100), index=True)
    room_type: Mapped[str] = mapped_column(Text)
    room_description: Mapped[str] = mapped_column(Text)
    location_id: Mapped[str] = mapped_column(String, ForeignKey('locations.id'))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    location = relationship("Location", back_populates="rooms")
    reservations = relationship("Reservation", back_populates="room", cascade="all, delete-orphan")
