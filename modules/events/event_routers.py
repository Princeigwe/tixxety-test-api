from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database_config import get_db

from . import event_services
from .dtos.create_event_dto import CreateEventDTO

router = APIRouter(prefix="/events", tags=["Events"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/")
async def create_event(event_dto: CreateEventDTO, db: Session = Depends(get_db)):
  return await event_services.create_event(event_dto, db)

@router.get("/")
async def get_events(db: Session = Depends(get_db)):
  return await event_services.get_events(db)

@router.get("/for-you")
async def get_events_for_you(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  return await event_services.get_events_for_you(token, db)