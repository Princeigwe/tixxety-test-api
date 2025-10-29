from database_config import Base
import uuid
from sqlalchemy import Column, String, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import date, datetime

from modules.tickets.ticket_entity import Ticket


class Event(Base):
  __tablename__ = "events"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  title: Mapped[str] = mapped_column(String(200))
  description: Mapped[str] = mapped_column(String(1000))
  start_date: Mapped[date] = mapped_column(Date)
  end_date: Mapped[date] = mapped_column(Date)
  street: Mapped[str] = mapped_column(String(300), nullable=True)
  city: Mapped[str] = mapped_column(String(100), nullable=True)
  state: Mapped[str] = mapped_column(String(100), nullable=True)
  country: Mapped[str] = mapped_column(String(100), nullable=True)
  total_tickets: Mapped[int] = mapped_column()
  tickets_sold: Mapped[int] = mapped_column(default=0)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

  tickets: Mapped[list["Ticket"]] = relationship(back_populates="event")
