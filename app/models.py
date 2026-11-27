from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    address = Column(String(255), nullable=False)
    joining_date = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    is_registered = Column(Boolean, default=False, nullable=False)