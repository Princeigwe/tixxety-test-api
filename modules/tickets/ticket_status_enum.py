from enum import Enum

class TicketStatusEnum(Enum):
  RESERVED = "reserved"
  PAID = "paid"
  EXPIRED = "expired"