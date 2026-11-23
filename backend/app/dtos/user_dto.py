from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.enums import UserRole


class UserRegisterDto(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    mobile_number: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")
    role: Optional[UserRole] = UserRole.USER


class UserLoginDto(BaseModel):
    email: EmailStr
    password: str


class UserUpdateDto(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    mobile_number: Optional[str] = Field(None, pattern=r"^\+?[0-9]{10,15}$")


class UserResponseDto(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    mobile_number: str
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponseDto(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponseDto
