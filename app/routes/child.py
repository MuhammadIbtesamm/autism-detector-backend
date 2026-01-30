from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.child import ChildCreate
from app.services.child_service import create_child, get_child_by_user
from app.utils.security import get_current_user_email
from app.models.user import User
from app.models.child import Child

router = APIRouter(prefix="/child", tags=["Child"])


# ================= DB DEPENDENCY =================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================= ADD CHILD =================
@router.post("/add")
def add_child(
    child: ChildCreate,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user_email),
):
    # Get logged-in user
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if user already has a child
    existing_child = get_child_by_user(db, user.id)
    if existing_child:
        raise HTTPException(status_code=400, detail="Child already exists")

    # Create new child
    new_child = create_child(db, child.name, child.age, child.gender, user.id)

    return {
        "id": new_child.id,
        "name": new_child.name,
        "age": new_child.age,
        "gender": new_child.gender,
        "message": "Child info saved successfully",
    }


# ================= GET MY CHILD =================
@router.get("/me")
def get_my_child(
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user_email),
):
    # Get logged-in user
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get child linked to this user
    child = db.query(Child).filter(Child.user_id == user.id).first()

    if not child:
        raise HTTPException(status_code=404, detail="No child found")

    return {
        "id": child.id,
        "name": child.name,
        "age": child.age,
        "gender": child.gender,
    }
