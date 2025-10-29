from database_config import Base
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import date, datetime

import typing

if typing.TYPE_CHECKING:
  from modules.events.event_entity import Event
  from modules.users.user_entity import User

from .ticket_status_enum import TicketStatusEnum


class Ticket(Base):
  __tablename__ = "tickets"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  status: Mapped[TicketStatusEnum] = mapped_column(Enum(TicketStatusEnum, name="ticket_status"), default=TicketStatusEnum.RESERVED)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

  event_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("events.id"))
  event: Mapped["Event"] = relationship(back_populates="tickets")

  user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
  user: Mapped["User"] = relationship(back_populates="tickets")