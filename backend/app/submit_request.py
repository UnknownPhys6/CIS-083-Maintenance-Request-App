from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional
import os
from pydantic import BaseModel



router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

'''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''
class CreateMaintenanceRequest(BaseModel):
    urgency: str
    type: str
    category: str
    description: str
    location: str
    images: str | None = None
    active: bool

# ------------------------------------------------------------
# Duplicate Request Detection
# ------------------------------------------------------------
def is_similar(description: str, existing_descriptions: List[str]) -> bool:
    description_words = set(description.lower().split())
    for old in existing_descriptions:
        old_words = set(old.lower().split())
        overlap = description_words & old_words
        if len(overlap) > 3:
            return True
    return False


# ------------------------------------------------------------
# POST /submit
# ------------------------------------------------------------
@router.post("/submit", response_model=SubmitResponse)
async def submit_request(
    location: str = Form(...),
    area_type: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    urgency: str = Form(...),
    images: Optional[List[UploadFile]] = File(None),
    #db: Session = Depends(get_db),
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
            file_path = os.path.join(UPLOAD_DIR, img.filename)
            with open(file_path, "wb") as f:
                f.write(contents)
            saved_filenames.append(img.filename)

    # ------------------------------------------------------------
    # Insert into the database
    # ------------------------------------------------------------
    new_request = MaintenanceRequest(
        location=location,
        area_type=area_type,
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