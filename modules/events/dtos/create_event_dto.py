from pydantic import BaseModel, Field
from datetime import datetime, date

class CreateEventDTO(BaseModel):
  title: str = Field(..., max_length=200, description="The title of the event")
  description: str = Field(..., max_length=1000, description="A detailed description of the event")
  start_date: date = Field(..., description="The start date of the event")
  end_date: date = Field(..., description="The end date of the event")
  street: str = Field(None, max_length=300, description="Street address of the event venue")
  city: str = Field(None, max_length=100, description="City where the event is located")
  state: str = Field(None, max_length=100, description="State where the event is located")
  country: str = Field(None, max_length=100, description="Country where the event is located")
  total_tickets: int = Field(..., gt=0, description="Total number of tickets available for the event")
