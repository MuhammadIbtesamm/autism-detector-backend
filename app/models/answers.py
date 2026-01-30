from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from datetime import datetime
from app.database import Base

class Answers(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    child_id = Column(Integer, ForeignKey("children.id"))
    answers = Column(String)  # "1,0,1,1,0,0,1,0,1,0"
    created_at = Column(DateTime, default=datetime.utcnow)
