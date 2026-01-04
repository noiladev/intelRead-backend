from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas

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
        password=user.password   # ❗ oddiy saqlaymiz
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

    if not db_user:
        raise HTTPException(status_code=400, detail="Email yoki parol xato")

    if db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Email yoki parol xato")

    return db_user
