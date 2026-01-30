from pydantic import BaseModel

class ChildCreate(BaseModel):
    name: str
    age: int
    gender: str
