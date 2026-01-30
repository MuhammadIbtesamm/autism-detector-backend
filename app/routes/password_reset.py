import random
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.models.password_reset import PasswordResetCode
from app.utils.email_service import send_verification_email
from app.schemas.password_reset import EmailRequest, CodeVerifyRequest
from app.utils.security import hash_password
from app.schemas.password_reset import PasswordUpdateRequest

router = APIRouter(prefix="/password-reset", tags=["Password Reset"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/send-code")
def send_code(data: EmailRequest, db: Session = Depends(get_db)):
    email = data.email
    print(f"📩 Password reset request for {email}")

    user = db.query(User).filter(User.email == email).first()
    message = {"message": "If the email exists, you'll get a verification code."}

    if not user:
        print("⚠️ Email not registered")
        return message

    code = str(random.randint(100000, 999999))
    expiry = datetime.utcnow() + timedelta(minutes=10)

    db.query(PasswordResetCode).filter(PasswordResetCode.email == email).delete()

    db_code = PasswordResetCode(email=email, code=code, expires_at=expiry)
    db.add(db_code)
    db.commit()

    print(f"📨 Generated code {code} for {email}")

    try:
        send_verification_email(email, code)
        print("✅ Email sent")
    except Exception as e:
        print("❌ Email sending failed:", str(e))

    return message



# 🔐 VERIFY CODE
@router.post("/verify-code")
def verify_code(data: CodeVerifyRequest, db: Session = Depends(get_db)):
    print(f"🔎 Verifying code for {data.email}")

    record = (
        db.query(PasswordResetCode)
        .filter(
            PasswordResetCode.email == data.email,
            PasswordResetCode.code == data.code,
            PasswordResetCode.expires_at > datetime.utcnow()
        )
        .first()
    )

    if not record:
        print("❌ Invalid or expired code")
        raise HTTPException(status_code=400, detail="Invalid or expired code")

    print("✅ Code verified successfully")
    return {"valid": True}

@router.post("/update-password")
def update_password(data: PasswordUpdateRequest, db: Session = Depends(get_db)):
    print("📥 Update password request:", data)

    record = (
        db.query(PasswordResetCode)
        .filter(
            PasswordResetCode.email == data.email,
            PasswordResetCode.code == data.code,
            PasswordResetCode.expires_at > datetime.utcnow()
        )
        .first()
    )

    if not record:
        return {"success": False, "message": "Invalid or expired code"}

    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        return {"success": False, "message": "User not found"}

    user.hashed_password = hash_password(data.new_password)

    db.delete(record)
    db.commit()

    return {"success": True, "message": "Password updated successfully"}
