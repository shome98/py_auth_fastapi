from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError,jwt
from passlib.context import CryptContext
from fastapi import Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from sqlalchemy.orm import Session
from app.db_connect import get_db_session
from app import models

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="api/login")

def get_password_hash(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict,expires_delta:Optional[timedelta]=None):
    to_encode=data.copy()
    expire=datetime.utcnow()+(expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,settings.JWT_SECRET,algorithm=settings.ALGORTHM)

def get_current_user(db: Session=Depends(get_db_session),token:str=Depends(oauth2_scheme)):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials😒",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload=jwt.decode(token,settings.JWT_SECRET,algorithms=[settings.ALGORTHM])
        email: str=payload.get("sub")
        if email is None:
            raise credentials_exception
    #  try using otehr exceptions
    except JWTError:
        raise credentials_exception
    user=db.query(models.User).filter(models.User.email==email).first()
    # raise exception on table not created
    if user is None:
        raise credentials_exception
    return user
