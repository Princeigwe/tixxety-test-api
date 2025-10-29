from datetime import date
from fastapi import Depends, HTTPException, status
from database_config import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import DatabaseError

from utils.jwt_encode_decode import decode_access_token

from .ticket_entity import Ticket 
from .dtos.reserve_ticket_dto import ReserveTicketDTO

from modules.users.user_entity import User
from modules.events import event_services
from modules.users import user_services


async def reserve_ticket(token: str, event_dto: ReserveTicketDTO, db: Session = Depends(get_db)) -> Ticket:
  try:
    decoded_token = await decode_access_token(token)
    user = await user_services.get_user_by_email(decoded_token['email'], db)

    event = await event_services.get_event_by_id(event_dto.event_id, db)
    if not event:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    
    existing_ticket = db.query(Ticket).filter(Ticket.event_id == event.id, Ticket.user_id == user.id).first()
    if existing_ticket:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has already reserved a ticket for this event")
    
    if event.tickets_sold >= event.total_tickets:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tickets available for this event")

    if date.today() > event.end_date:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot reserve ticket for past event")
    
    await event_services.update_event_tickets_sold_count(event.id, db)

    ticket = Ticket(event_id=event.id, user_id=user.id)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket
  except Exception as e:
    if isinstance(e, HTTPException):
      raise e
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_user_tickets(token: str, db: Session = Depends(get_db)) -> list[Ticket]:
  try:
    decoded_token = await decode_access_token(token)
    user = await user_services.get_user_by_email(decoded_token['email'], db)
    tickets = db.query(Ticket).filter(Ticket.user_id == user.id).all()
    return tickets
  except Exception as e:
    if isinstance(e, HTTPException):
      raise e
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))