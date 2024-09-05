from sqlalchemy import Integer, String, Text, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.database import Base

class Location(Base):
    __tablename__ = 'locations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(Text)
    city: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    rooms = relationship("Room", back_populates="location", cascade="all, delete-orphan")


from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Room(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_number: Mapped[int] = mapped_column(String(100), index=True)
    room_type: Mapped[str] = mapped_column(Text)
    room_description: Mapped[str] = mapped_column(Text)
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey('locations.id'))  # ForeignKey to locations
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # Relationship with Location
    location = relationship("Location", back_populates="rooms")