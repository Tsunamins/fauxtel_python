from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.database import Base
import uuid


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    phone_number = Column(String)

    reservations = relationship("Reservation", back_populates="user")


