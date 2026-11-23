from typing import Optional
from pydantic import BaseModel, Field


class PassengerCreateDto(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=1, le=120)
    gender: str = Field(..., pattern=r"^(MALE|FEMALE|OTHER|Male|Female|Other)$")
    mobile_number: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")


class PassengerUpdateDto(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=1, le=120)
    gender: Optional[str] = None
    mobile_number: Optional[str] = None


class PassengerResponseDto(BaseModel):
    id: int
    user_id: int
    name: str
    age: int
    gender: str
    mobile_number: str

    class Config:
        from_attributes = True
