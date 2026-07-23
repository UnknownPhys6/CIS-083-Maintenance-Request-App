from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional
from sqlalchemy.orm import Session
import os

from .db import SessionLocal
from .model import MaintenanceRequest
from .schemas import SubmitResponse

router = APIRouter()


upload_dir = "uploads"
os.makedirs(upload_dir, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------------------------------------------
# Duplicate Request Detection
# ------------------------------------------------------------
def is_similar(description: str, existing_descriptions: List[str]) -> bool:
    description_words = set(description.lower().split())
    for old in existing_descriptions:
        old_words = set(old.lower().split())
        overlap = description_words & old_words
        if len(overlap) > 6:
            return True
    return False


# ------------------------------------------------------------
# POST /submit
# ------------------------------------------------------------
@router.post("/submit", response_model=SubmitResponse)
async def submit_request(
    location: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    urgency: str = Form(...),
    images: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db),
):
    # ------------------------------------------------------------
    # Duplicate check — query existing requests at this location
    # ------------------------------------------------------------
    existing = db.query(MaintenanceRequest).filter(
        MaintenanceRequest.location == location
    ).all()
    existing_descriptions = [r.description for r in existing]
    
    if is_similar(description, existing_descriptions):
        raise HTTPException(status_code=400, detail="Request already exists")

    # ------------------------------------------------------------
    # Save uploaded images to disk, keep filenames for the DB
    # ------------------------------------------------------------
    saved_filenames = []
    if images:
        for img in images:
            contents = await img.read()
            file_path = os.path.join(upload_dir, img.filename)
            with open(file_path, "wb") as f:
                f.write(contents)
            saved_filenames.append(img.filename)

    # ------------------------------------------------------------
    # Insert into the database
    # ------------------------------------------------------------
    new_request = MaintenanceRequest(
        location=location,
        category=category,
        description=description,
        urgency=urgency,
        stage="Submitted",
        active=True,
        images=",".join(saved_filenames) if saved_filenames else None,
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return SubmitResponse(request_id=new_request.id, message="Request submitted successfully")