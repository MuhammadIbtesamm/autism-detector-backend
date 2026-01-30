from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timedelta
from app.database import Base


class PasswordResetCode(Base):
    __tablename__ = "password_reset_codes"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    code = Column(String, index=True)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=10))
