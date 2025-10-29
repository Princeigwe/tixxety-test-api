from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database_config import get_db

from modules.users.dtos.create_user_dto import CreateUserDTO

from . import auth_services

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(user_dto: CreateUserDTO, db: Session = Depends(get_db)):
  return await auth_services.register_user(user_dto, db)


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  return await auth_services.authenticate_user(form_data.username, form_data.password, db)