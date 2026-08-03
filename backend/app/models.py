from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from db import Base

class CreateMaintenanceRequest(BaseModel):
    id: int
    location: str
    category: str
    description: str
    urgency: str
    stage: str
    active: bool
    tech_description: Optional[str] = None
    images: Optional[str] = None

class Config:
        from_attributes = True


class UpdateRequest(BaseModel):
    tech_description: Optional[str] = None
    stage: Optional[str] = None

class SubmitResponse(BaseModel):
    request_id: int
    message: str

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    hashedpass = Column(String(255), nullable=False)

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    expires = Column(DateTime, nullable=False)