from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.database import Base
import uuid

class Location(Base):
    __tablename__ = 'locations'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(Text)
    city: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    rooms = relationship("Room", back_populates="location", cascade="all, delete-orphan")
