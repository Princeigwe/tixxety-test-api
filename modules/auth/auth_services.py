from fastapi import Depends, HTTPException, status
from database_config import get_db
from passlib.context import CryptContext

from sqlalchemy.orm import Session


from modules.users.dtos.create_user_dto import CreateUserDTO
from modules.users.user_services import create_user


async def register_user(body: CreateUserDTO, db: Session = Depends(get_db)):
    cipher = CryptContext(schemes='sha256_crypt')
    hashed_password = cipher.hash(body.password)
    body.password = hashed_password
    return await create_user(body, db)
