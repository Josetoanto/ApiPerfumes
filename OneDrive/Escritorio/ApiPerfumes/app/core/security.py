from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    if not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "INVALID_PASSWORD", "message": "La contraseña no puede estar vacía"}
        )
    try:
        return pwd_context.hash(password)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_code": "HASH_ERROR", "message": "Error al encriptar la contraseña"}
        )


def verify_password(password: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(password, hashed)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_code": "VERIFY_ERROR", "message": "Error al verificar la contraseña"}
        )


def create_access_token(data: dict, expires_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES):
    if not data or "sub" not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "INVALID_TOKEN_DATA", "message": "Datos inválidos para generar token"}
        )

    try:
        expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
        to_encode = data.copy()
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow()
        })

        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_code": "TOKEN_ERROR", "message": "Error al generar el token JWT"}
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_code": "SERVER_ERROR", "message": "Error interno al generar token"}
        )
