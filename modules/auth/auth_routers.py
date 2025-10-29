from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database_config import get_db

from modules.users.dtos.create_user_dto import CreateUserDTO
from .auth_services import register_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(user_dto: CreateUserDTO, db: Session = Depends(get_db)):
    return await register_user(user_dto, db)
