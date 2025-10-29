from fastapi import Depends, HTTPException, status
from database_config import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import DatabaseError

from .dtos.create_user_dto import CreateUserDTO
from .user_entity import User


async def create_user(user_dto: CreateUserDTO, db: Session = Depends(get_db)) -> User:
  try:
    existing_user = db.query(User).filter(User.email == user_dto.email).first()
    if existing_user:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    new_user = User(
      name=user_dto.name,
      email=user_dto.email,
      password=user_dto.password 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
  except DatabaseError as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))