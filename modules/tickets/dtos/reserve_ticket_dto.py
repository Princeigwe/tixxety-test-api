from pydantic import BaseModel, Field

class ReserveTicketDTO(BaseModel):
    event_id: str = Field(..., description="The ID of the event for which the ticket is being reserved")