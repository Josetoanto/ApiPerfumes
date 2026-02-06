from sqlalchemy.orm import Session
from app.modules.users.model import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings


def register_user(db: Session, data):
    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, data):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        return None

    token = create_access_token(
        {"sub": str(user.id)},
        settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return token
