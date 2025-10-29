from datetime import date
from fastapi import Depends, HTTPException, status
from database_config import get_db, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from utils.jwt_encode_decode import decode_access_token

from .ticket_entity import Ticket 
from .dtos.reserve_ticket_dto import ReserveTicketDTO
from .ticket_status_enum import TicketStatusEnum

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


async def pay_for_ticket(token: str, ticket_id: str, db: Session = Depends(get_db)) -> Ticket:
  try:
    decoded_token = await decode_access_token(token)
    user = await user_services.get_user_by_email(decoded_token['email'], db)

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id, Ticket.user_id == user.id).first()
    if not ticket:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    ticket.status = TicketStatusEnum.PAID
    db.commit()
    db.refresh(ticket)
    return ticket
  except Exception as e:
    if isinstance(e, HTTPException):
      raise e
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def expire_unpaid_tickets():
  try:
    print("Running expire_unpaid_tickets task...")
    db = SessionLocal()
    cutoff_time = datetime.now() - timedelta(minutes=2) # setting cutoff time for unpaid tickets to 2 minutes ago
    unpaid_tickets = db.query(Ticket).filter(Ticket.status == TicketStatusEnum.RESERVED, Ticket.created_at < cutoff_time).all()
    for ticket in unpaid_tickets:
      ticket.status = TicketStatusEnum.EXPIRED
    db.commit()
    print(f"Expired {len(unpaid_tickets)} unpaid tickets.")
  except Exception as e:
    if isinstance(e, HTTPException):
      raise e
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))