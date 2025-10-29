from pydantic import BaseModel, EmailStr, Field


class CreateUserDTO(BaseModel):
  email: EmailStr = Field(..., description="The user's email address")
  password: str = Field(..., min_length=8, description="The user's password")
  name: str = Field(..., max_length=100, description="The user's full name")
  street: str | None = Field(None, max_length=300, description="The user's street address")
  city: str | None = Field(None, max_length=100, description="The user's city")
  state: str | None = Field(None, max_length=100, description="The user's state")
  country: str | None = Field(None, max_length=100, description="The user's country")