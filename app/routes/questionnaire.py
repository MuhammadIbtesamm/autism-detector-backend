from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.questionnaire import QuestionnaireCreate
from app.models.answers import Answers
from app.models.child import Child
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/questionnaire", tags=["Questionnaire"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/submit")
def submit_answers(
    data: QuestionnaireCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    # Make sure child belongs to logged-in user
    child = db.query(Child).filter(
        Child.id == data.child_id,
        Child.user_id == user.id
    ).first()

    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    # Convert list → string for DB
    answers_string = ",".join(map(str, data.answers))

    new_entry = Answers(
        user_id=user.id,
        child_id=data.child_id,
        answers=answers_string
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return {
        "message": "Answers submitted successfully",
        "saved_answers": answers_string
    }
