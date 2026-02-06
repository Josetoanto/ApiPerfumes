from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.modules.perfumes.schemas import PerfumeCreate, PerfumeResponse
from app.modules.perfumes.service import (
    get_perfumes,
    create_perfume,
    update_perfume,
    delete_perfume
)

router = APIRouter(prefix="/perfumes", tags=["Perfumes"])

@router.get("/", response_model=list[PerfumeResponse])
def list_perfumes(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_perfumes(db, current_user.id)

@router.post("/", response_model=PerfumeResponse)
def add_perfume(
    data: PerfumeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_perfume(db, current_user.id, data)

@router.put("/{perfume_id}", response_model=PerfumeResponse)
def edit_perfume(
    perfume_id: int,
    data: PerfumeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    perfume = update_perfume(db, current_user.id, perfume_id, data)
    if not perfume:
        raise HTTPException(status_code=404, detail="Perfume no encontrado")
    return perfume

@router.delete("/{perfume_id}")
def remove_perfume(
    perfume_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not delete_perfume(db, current_user.id, perfume_id):
        raise HTTPException(status_code=404, detail="Perfume no encontrado")
    return {"message": "Perfume eliminado"}
