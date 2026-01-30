from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

BCRYPT_MAX_BYTES = 72  # bcrypt limit

def hash_password(password: str) -> str:
    return pwd_context.hash(password[:BCRYPT_MAX_BYTES])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password[:BCRYPT_MAX_BYTES], hashed_password)
