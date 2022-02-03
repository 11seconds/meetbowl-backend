from typing import Optional

from pydantic import BaseModel, EmailStr

from uuid import uuid4

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: Optional[EmailStr] = None
    

# Properties to receive via API on update
class UserUpdate(UserBase):
    nickname: Optional[str]


class UserInDBBase(UserBase):
    id: str
    is_active: bool
    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
    kakao_id: int
    is_superuser: bool = False
