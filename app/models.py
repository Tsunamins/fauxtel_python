from sqlalchemy import Integer, String, Text, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.database import Base
import uuid

class Location(Base):
    __tablename__ = 'locations'

    id: Mapped[int] = Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
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

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    room_number: Mapped[int] = mapped_column(String(100), index=True)
    room_type: Mapped[str] = mapped_column(Text)
    room_description: Mapped[str] = mapped_column(Text)
    location_id: Mapped[str] = mapped_column(String, ForeignKey('locations.id'))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # Relationship with Location
    location = relationship("Location", back_populates="rooms")


from sqlalchemy import Integer, String, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Reservation(Base):
    __tablename__ = 'reservations'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    reservation_code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    room_id: Mapped[str] = mapped_column(String, ForeignKey('rooms.id'))
    location_id: Mapped[str] = mapped_column(String, ForeignKey('locations.id'))
    room_id: Mapped[str] = mapped_column(String, ForeignKey('rooms.id'))
    date_ranges: Mapped[list] = mapped_column(JSON)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    modified_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    room = relationship("Room", back_populates="reservations")
    location = relationship("Location")

# Add this to Room model:
Room.reservations = relationship("Reservation", back_populates="room", cascade="all, delete-orphan")


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    phone_number = Column(String)

    reservations = relationship("Reservation", back_populates="user")
