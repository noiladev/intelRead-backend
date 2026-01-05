from fastapi import FastAPI, Depends
import models, database, schemas, auth
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # vaqtincha
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register endpoint
# @app.post("/register")
# def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
#     new_user = auth.register_user(user, db)
#     return {"message": "User registered successfully", "user_id": new_user.id}

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    new_user = auth.register_user(user, db)

    access_token = auth.create_access_token(
        {"sub": new_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Login endpoint
@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = auth.login_user(user, db)
    return {"message": "Login successful", "user_id": db_user.id}

import os

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)