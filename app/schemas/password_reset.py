from pydantic import BaseModel, EmailStr

class EmailRequest(BaseModel):
    email: EmailStr

class CodeVerifyRequest(BaseModel):
    email: EmailStr
    code: str

class PasswordUpdateRequest(BaseModel):
    email: EmailStr
    code: str
    new_password: str
