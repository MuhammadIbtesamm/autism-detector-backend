from sqlalchemy.orm import Session
from app.models.child import Child

def create_child(db: Session, name: str, age: int, gender: str, user_id: int):
    child = Child(name=name, age=age, gender=gender, user_id=user_id)
    db.add(child)
    db.commit()
    db.refresh(child)
    return child

def get_child_by_user(db: Session, user_id: int):
    return db.query(Child).filter(Child.user_id == user_id).first()
