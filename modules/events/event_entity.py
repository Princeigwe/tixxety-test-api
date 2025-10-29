from database_config import Base
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class Event(Base):
  __tablename__ = "events"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  title: Mapped[str] = mapped_column(String(200))
  description: Mapped[str] = mapped_column(String(1000))
  start_date: Mapped[datetime] = mapped_column(DateTime)
  end_date: Mapped[datetime] = mapped_column(DateTime)
  venue: Mapped[str] = mapped_column(String(300))
  total_tickets: Mapped[int] = mapped_column()
  tickets_sold: Mapped[int] = mapped_column(default=0)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)