from sqlalchemy import Column, Integer, String, Boolean, Date
from .db import Base

class MaintenanceRequest(Base):
    __tablename__ =  "maintenance_requests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    location = Column(String(255))
    area_type = Column(String(50))
    category = Column(String(100))
    description = Column(String(1000))
    urgency = Column(String(10))
    stage = Column(String(50), default="Submitted")
    active = Column(Boolean, default=True)
    tech_description = Column(String(1000), nullable=True)
    images = Column(String(1000), nullable=True)
   # date = Column(Date)