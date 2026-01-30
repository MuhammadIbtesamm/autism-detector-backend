from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import SessionLocal
from app.services.ml_service import predict_autism_risk
from app.schemas.prediction import PredictionRequest
from app.utils.security import get_current_user_email
from app.models.user import User
from app.models.child import Child
from app.models.prediction_result import PredictionResult

router = APIRouter(prefix="/prediction", tags=["Prediction"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/predict")
def predict(data: PredictionRequest,
            db: Session = Depends(get_db),
            user_email: str = Depends(get_current_user_email)):

    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    child = db.query(Child).filter(Child.user_id == user.id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    probability = predict_autism_risk(data.answers, child.age)
    percent = round(probability * 100, 2)

    if percent < 30:
        level = "Low"
    elif percent < 70:
        level = "Medium"
    else:
        level = "High"

    # Save result
    result = PredictionResult(
        user_id=user.id,
        child_id=child.id,
        probability_percent=percent,
        risk_level=level,
        created_at=datetime.utcnow()
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return {
        "autism_probability_percent": percent,
        "risk_level": level
    }


@router.get("/history")
def get_prediction_history(
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user_email)
):
    user = db.query(User).filter(User.email == user_email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    results = (
        db.query(PredictionResult)
        .filter(PredictionResult.user_id == user.id)
        .order_by(PredictionResult.created_at.desc())
        .all()
    )

    history = []

    for r in results:
        child = db.query(Child).filter(Child.id == r.child_id).first()

        history.append({
            "child_name": child.name if child else "Unknown",
            "child_age": child.age if child else "—",
            "child_gender": child.gender if child else "—",
            "probability_percent": r.probability_percent,
            "risk_level": r.risk_level,
            "created_at": r.created_at,
        })

    return {
        "user_email": user.email,
        "history": history
    }
