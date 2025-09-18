"""User schemas for API requests and responses"""

from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema"""

    email: EmailStr
    name: str


class UserCreate(UserBase):
    """Schema for creating a new user"""

    password: str


class UserUpdate(BaseModel):
    """Schema for updating a user"""

    email: EmailStr | None = None
    name: str | None = None
    status: str | None = None


class UserResponse(UserBase):
    """Schema for user responses"""

    id: int
    uuid: str
    status: str
    is_superuser: bool
    last_login: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login"""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for authentication token"""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token data"""

    email: str | None = None
