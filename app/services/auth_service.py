from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.hashing import hash_password, verify_password

BCRYPT_MAX_BYTES = 72  # bcrypt limit

def create_user(db: Session, email: str, password: str):
    safe_password = password[:BCRYPT_MAX_BYTES]  # 🔧 truncate before hashing
    hashed_pw = hash_password(safe_password)

    user = User(email=email, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    safe_password = password[:BCRYPT_MAX_BYTES]  # 🔧 same truncation when verifying

    if not verify_password(safe_password, user.hashed_password):
        return None

    return user
