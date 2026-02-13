from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.dependencies import get_db, get_current_user
from app.modules.perfumes.schemas import PerfumeCreate, PerfumeResponse
from app.modules.perfumes.service import (
    get_perfumes,
    create_perfume,
    update_perfume,
    delete_perfume
)

router = APIRouter(prefix="/perfumes", tags=["Perfumes"])

def handle_db_error(exc: Exception):
    if isinstance(exc, IntegrityError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "DB_CONSTRAINT", "message": "Violación de integridad en la base de datos"}
        )
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={"error_code": "UNKNOWN_ERROR", "message": "Error interno del servidor"}
    )

@router.get("/", response_model=list[PerfumeResponse])
def list_perfumes(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        return get_perfumes(db, current_user.id)
    except Exception as e:
        handle_db_error(e)

@router.post("/", response_model=PerfumeResponse)
def add_perfume(data: PerfumeCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        return create_perfume(db, current_user.id, data)
    except Exception as e:
        handle_db_error(e)

@router.put("/{perfume_id}", response_model=PerfumeResponse)
def edit_perfume(perfume_id: int, data: PerfumeCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        perfume = update_perfume(db, current_user.id, perfume_id, data)
        if not perfume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error_code": "NOT_FOUND", "message": "Perfume no encontrado"}
            )
        return perfume
    except Exception as e:
        handle_db_error(e)

@router.delete("/{perfume_id}")
def remove_perfume(perfume_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        if not delete_perfume(db, current_user.id, perfume_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error_code": "NOT_FOUND", "message": "Perfume no encontrado"}
            )
        return {"message": "Perfume eliminado"}
    except Exception as e:
        handle_db_error(e)
