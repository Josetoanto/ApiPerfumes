from sqlalchemy.orm import Session
from app.modules.perfumes.model import Perfume

def get_perfumes(db: Session, user_id: int):
    return db.query(Perfume).filter(Perfume.user_id == user_id).all()

def create_perfume(db: Session, user_id: int, data):
    perfume = Perfume(
        user_id=user_id,
        **data.dict()
    )
    db.add(perfume)
    db.commit()
    db.refresh(perfume)
    return perfume

def update_perfume(db: Session, user_id: int, perfume_id: int, data):
    perfume = db.query(Perfume).filter(
        Perfume.id == perfume_id,
        Perfume.user_id == user_id
    ).first()

    if not perfume:
        return None

    for key, value in data.dict().items():
        setattr(perfume, key, value)

    db.commit()
    return perfume

def delete_perfume(db: Session, user_id: int, perfume_id: int):
    perfume = db.query(Perfume).filter(
        Perfume.id == perfume_id,
        Perfume.user_id == user_id
    ).first()

    if not perfume:
        return False

    db.delete(perfume)
    db.commit()
    return True
