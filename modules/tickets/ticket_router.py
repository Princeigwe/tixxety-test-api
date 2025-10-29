from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database_config import get_db
from . import ticket_services
from .dtos.reserve_ticket_dto import ReserveTicketDTO

router = APIRouter(prefix="/tickets", tags=["Tickets"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/")
async def reserve_ticket(event_dto: ReserveTicketDTO, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await ticket_services.reserve_ticket(token, event_dto, db)