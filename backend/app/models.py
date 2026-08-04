
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Boolean
from db import Base

class MaintenanceRequest(Base):
    __tablename__ =  "maintenance_requests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    location = Column(String(255))
    category = Column(String(100))
    description = Column(String(1000))
    urgency = Column(String(10))
    stage = Column(String(50), default="Submitted")
    active = Column(Boolean, default=True)
    tech_description = Column(String(1000), nullable=True)
    images = Column(String(1000), nullable=True)
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