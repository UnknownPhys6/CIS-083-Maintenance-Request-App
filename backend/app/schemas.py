from pydantic import BaseModel
from typing import Optional


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