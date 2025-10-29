from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from database_config import get_db

from . import event_services
from .dtos.create_event_dto import CreateEventDTO

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/")
async def create_event(event_dto: CreateEventDTO, db: Session = Depends(get_db)):
  return await event_services.create_event(event_dto, db)

