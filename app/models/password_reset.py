from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime, timedelta
from app.database import Base


class PasswordResetCode(Base):
    __tablename__ = "password_reset_codes"

    id = Column(Integer, primary_key=True, index=True)

    # Store email normalized (lowercase) when saving
    email = Column(String, index=True, nullable=False)

    # 🔐 Store HASHED code, not plain text
    code_hash = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    expires_at = Column(
        DateTime,
        default=lambda: datetime.utcnow() + timedelta(minutes=10),
        nullable=False
    )

    # ✅ Mark code as used so it can't be reused
    is_used = Column(Boolean, default=False, nullable=False)
