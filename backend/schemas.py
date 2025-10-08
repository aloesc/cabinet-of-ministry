from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime, date



# ---------- USERS ----------
class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phonenumber: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Literal["male", "female", "other"]] = None
    role: Optional[str] = None

class UserForgotPassword(BaseModel):
    email: EmailStr

class UserResetPassword(BaseModel):
    new_password: str

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None
    phonenumber: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    role: Optional[str] = None


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    phonenumber: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    role: Optional[str] = None
    is_superuser: Optional[bool] = None



# ---------- EVENTS ----------
class EventBase(BaseModel):
    title: str
    description: str
    date_of_event: Optional[datetime] = None
    location: Optional[date] = None
    type_of_event: Optional[str] = None


class EventCreate(EventBase):
    title: str
    description: Optional[str] = None
    date_of_event: Optional[datetime] = None
    location: Optional[str] = None
    type_of_event: str


class EventRead(EventBase):
    id: int

    class Config:
        orm_mode = True


# ---------- DOCUMENTS ----------
class DocumentBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date_of_uploaded: Optional[datetime] = None
    type_of_document: Optional[str] = None
    binary_data: Optional[str] = None


class DocumentRead(DocumentBase):
    id: int
    can_edit: bool

    class Config:
        orm_mode = True
