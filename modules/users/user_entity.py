from database_config import Base
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from modules.tickets.ticket_entity import Ticket

class User(Base):
  __tablename__ = "users"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name: Mapped[str] = mapped_column(String(100))
  email: Mapped[str] = mapped_column(String(150), unique=True)
  password: Mapped[str] = mapped_column(String(255))
  created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

  tickets: Mapped[list["Ticket"]] = relationship(back_populates="user")
