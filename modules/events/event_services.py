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
      street=event_dto.street,
      city=event_dto.city,
      state=event_dto.state,
      country=event_dto.country,
      total_tickets=event_dto.total_tickets
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event
  except Exception as e:
    if isinstance(e, HTTPException):
      raise e
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_events(db: Session = Depends(get_db)) -> list[Event]:
  try:
    events = db.query(Event).all()
    return events
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_event_by_id(event_id: int, db: Session = Depends(get_db)) -> Event:
  try:
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event
  except Exception as e:
    if isinstance(e, HTTPException):
      raise e
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def update_event_tickets_sold_count(event_id: str, db: Session = Depends(get_db)):
  try:
    event = await get_event_by_id(event_id, db)
    event.tickets_sold += 1
    db.commit()
  except DatabaseError as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update tickets sold")