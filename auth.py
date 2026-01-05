from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas

from datetime import datetime, timedelta
from jose import jwt

# JWT SETTINGS
SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_THIS"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# REGISTER
def register_user(user: schemas.UserCreate, db: Session):
    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        email=user.email,
        password=user.password  # hozircha oddiy
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# LOGIN
def login_user(user: schemas.UserLogin, db: Session):
    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Email yoki parol xato")

    return db_user
