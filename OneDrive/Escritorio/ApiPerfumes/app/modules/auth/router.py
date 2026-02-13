from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.dependencies import get_db
from app.modules.auth.schemas import RegisterRequest, LoginRequest
from app.modules.auth.service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])

def raise_http_error(status_code: int, error_code: str, message: str):
    raise HTTPException(
        status_code=status_code,
        detail={"error_code": error_code, "message": message}
    )

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        return register_user(db, data)
    except IntegrityError:
        raise_http_error(
            status.HTTP_400_BAD_REQUEST,
            "USER_EXISTS",
            "El usuario ya está registrado"
        )
    except Exception:
        raise_http_error(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "SERVER_ERROR",
            "Error interno del servidor"
        )

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        token = login_user(db, data)
        if not token:
            raise_http_error(
                status.HTTP_401_UNAUTHORIZED,
                "INVALID_CREDENTIALS",
                "Credenciales inválidas"
            )
        return {"access_token": token}
    except Exception:
        raise_http_error(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "SERVER_ERROR",
            "Error interno del servidor"
        )
