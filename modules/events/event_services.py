from fastapi import Depends, HTTPException, status
from database_config import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import DatabaseError

from .dtos.create_event_dto import CreateEventDTO
from .event_entity import Event




async def create_event(event_dto: CreateEventDTO, db: Session = Depends(get_db)) -> Event:
  try:
    existing_event = db.query(Event).filter(Event.title == event_dto.title, Event.start_date == event_dto.start_date).first()
    if existing_event:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An event with the same title and start date already exists")
    new_event = Event(
      title=event_dto.title,
      description=event_dto.description,
      start_date=event_dto.start_date,
      end_date=event_dto.end_date,
      venue=event_dto.venue,
      total_tickets=event_dto.total_tickets
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event
  except Exception as e:
    if isinstance(e, HTTPException):
      raise e
    elif isinstance(e, DatabaseError):
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
