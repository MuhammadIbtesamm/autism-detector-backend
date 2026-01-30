from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class PredictionResult(Base):
    __tablename__ = "prediction_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    child_id = Column(Integer, ForeignKey("children.id"))

    probability_percent = Column(Float)
    risk_level = Column(String)
    created_at = Column(DateTime)

    # 🔥 THIS IS WHAT YOU WERE MISSING
    child = relationship("Child")
    user = relationship("User")
