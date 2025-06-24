from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, auth
from app.db_connect import get_db_session

router=APIRouter()

@router.post("api/register",response_model=schemas.User)
def register(user: schemas.UserCreate,db: Session=Depends(get_db_session)):
    # check if table does not exist create one
    existing_user=db.query(models.User).filter(models.User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email is already registered😒")
    hashed_password=auth.get_password_hash(user.password)
    # username=user.email[:4] if user.username is None else user.username
    new_user=models.User(username=user.username,email=user.email,hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/api/login", response_model=schemas.Token)
def login(form_data: schemas.Login, db: Session = Depends(get_db_session)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token=auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/api/profile", response_model=schemas.User)
def profile(current_user: models.User = Depends(auth.get_current_user)):
    return current_user