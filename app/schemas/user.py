from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        extra="forbid",
        validate_assignment=True,
    )
    email: EmailStr 
    name: str 
    created_at: datetime = Field(default_factory=datetime.now)



class UserResponse(UserBase):
    id: UUID
    auth0_id: str
