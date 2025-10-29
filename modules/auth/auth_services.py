from fastapi import Depends, HTTPException, status
from database_config import get_db
from passlib.context import CryptContext

from sqlalchemy.orm import Session

from modules.users.dtos.create_user_dto import CreateUserDTO
from modules.users import user_services

from utils.jwt_encode_decode import create_access_token, decode_access_token


async def register_user(body: CreateUserDTO, db: Session = Depends(get_db)):
  cipher = CryptContext(schemes='sha256_crypt')
  hashed_password = cipher.hash(body.password)
  body.password = hashed_password
  return await user_services.create_user(body, db)


async def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
  cipher = CryptContext(schemes='sha256_crypt')
  user =  await user_services.get_user_by_email(email, db)
  if not user or not cipher.verify(password, user.password):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
  token = await create_access_token({"user_id": str(user.id), "email": user.email, "name": user.name})
  return{
    "user": user,
    "access_token": token, 
    "token_type": "bearer"
  }