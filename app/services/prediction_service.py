from sqlalchemy.orm import Session
from app.models.prediction_result import PredictionResult

def save_prediction_result(db: Session, user_id: int, child_id: int, percent: float, level: str):
    result = PredictionResult(
        user_id=user_id,
        child_id=child_id,
        probability_percent=percent,
        risk_level=level
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
