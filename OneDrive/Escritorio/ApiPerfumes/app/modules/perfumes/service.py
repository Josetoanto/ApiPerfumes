from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.modules.perfumes.model import Perfume


def get_perfumes(db: Session, user_id: int):
    try:
        perfumes = db.query(Perfume).filter(Perfume.user_id == user_id).all()
        return perfumes
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_code": "SERVER_ERROR", "message": "Error al obtener perfumes"}
        )


def create_perfume(db: Session, user_id: int, data):
    try:
        perfume = Perfume(user_id=user_id, **data.dict())
        db.add(perfume)
        db.commit()
        db.refresh(perfume)
        return perfume
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "DB_CONSTRAINT", "message": "Error de integridad al crear perfume"}
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_code": "SERVER_ERROR", "message": "Error interno al crear perfume"}
        )


def update_perfume(db: Session, user_id: int, perfume_id: int, data):
    perfume = db.query(Perfume).filter(
        Perfume.id == perfume_id,
        Perfume.user_id == user_id
    ).first()

    if not perfume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NOT_FOUND", "message": "Perfume no encontrado"}
        )

    try:
        for key, value in data.dict().items():
            setattr(perfume, key, value)
        db.commit()
        db.refresh(perfume)
        return perfume
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_code": "SERVER_ERROR", "message": "Error interno al actualizar perfume"}
        )


def delete_perfume(db: Session, user_id: int, perfume_id: int):
    perfume = db.query(Perfume).filter(
        Perfume.id == perfume_id,
        Perfume.user_id == user_id
    ).first()

    if not perfume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NOT_FOUND", "message": "Perfume no encontrado"}
        )

    try:
        db.delete(perfume)
        db.commit()
        return {"message": "Perfume eliminado"}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_code": "SERVER_ERROR", "message": "Error interno al eliminar perfume"}
        )
