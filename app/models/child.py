from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
