import random
import hashlib
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.models.password_reset import PasswordResetCode
from app.utils.email_service import send_verification_email
from app.schemas.password_reset import EmailRequest, CodeVerifyRequest, PasswordUpdateRequest
from app.utils.security import hash_password

router = APIRouter(prefix="/password-reset", tags=["Password Reset"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_code(code: str) -> str:
    return hashlib.sha256(code.encode()).hexdigest()


# 📩 SEND CODE
@router.post("/send-code")
def send_code(data: EmailRequest, db: Session = Depends(get_db)):
    email = data.email.lower().strip()
    message = {"message": "If the email exists, you'll get a verification code."}

    user = db.query(User).filter(User.email == email).first()
    if not user:
        return message

    code = str(random.randint(100000, 999999))
    expiry = datetime.utcnow() + timedelta(minutes=10)

    # Remove old codes
    db.query(PasswordResetCode).filter(PasswordResetCode.email == email).delete()

    db_code = PasswordResetCode(
        email=email,
        code_hash=hash_code(code),
        expires_at=expiry
    )
    db.add(db_code)
    db.commit()

    try:
        send_verification_email(email, code)
    except Exception:
        pass  # Don't expose email errors

    return message


# 🔐 VERIFY CODE
@router.post("/verify-code")
def verify_code(data: CodeVerifyRequest, db: Session = Depends(get_db)):
    email = data.email.lower().strip()
    code_hash = hash_code(data.code)

    record = (
        db.query(PasswordResetCode)
        .filter(
            PasswordResetCode.email == email,
            PasswordResetCode.code_hash == code_hash,
            PasswordResetCode.expires_at > datetime.utcnow(),
            PasswordResetCode.is_used == False
        )
        .first()
    )

    if not record:
        raise HTTPException(status_code=400, detail="Invalid or expired code")

    return {"valid": True}


# 🔑 UPDATE PASSWORD
@router.post("/update-password")
def update_password(data: PasswordUpdateRequest, db: Session = Depends(get_db)):
    email = data.email.lower().strip()
    code_hash = hash_code(data.code)

    record = (
        db.query(PasswordResetCode)
        .filter(
            PasswordResetCode.email == email,
            PasswordResetCode.code_hash == code_hash,
            PasswordResetCode.expires_at > datetime.utcnow(),
            PasswordResetCode.is_used == False
        )
        .first()
    )

    if not record:
        raise HTTPException(status_code=400, detail="Invalid or expired code")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = hash_password(data.new_password)

    # Mark code as used instead of deleting (audit trail)
    record.is_used = True

    db.commit()

    return {"success": True, "message": "Password updated successfully"}
