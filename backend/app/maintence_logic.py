from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from typing import List, Optional
from .schemas import CreateMaintenanceRequest
from sqlalchemy.orm import Session
from .db import SessionLocal

import os

from .model import MaintenanceRequest


router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/get_maintenance_request_by_id/{id}", response_model=CreateMaintenanceRequest)
async def get_single_request(id: int, db: Session = Depends(get_db)):
    request = db.query(MaintenanceRequest).filter(MaintenanceRequest.id == id).first()
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return request


@router.put("/request/{id}", response_model=CreateMaintenanceRequest)
async def save_tech_report(
    id: int,
    tech_description: str = Form(...),
    stage: str = Form(...),
    images: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db),
):
    request = db.query(MaintenanceRequest).filter(MaintenanceRequest.id == id).first()
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")

    saved_filenames = []
    if images:
        for img in images:
            contents = await img.read()
            file_path = os.path.join(UPLOAD_DIR, img.filename)
            with open(file_path, "wb") as f:
                f.write(contents)
            saved_filenames.append(img.filename)

    request.tech_description = tech_description
    request.stage = stage
    request.active = (stage != "Completed")
    if saved_filenames:
        request.images = ",".join(saved_filenames)

    db.commit()
    db.refresh(request)

    return request


@router.get("/requests", response_model=List[CreateMaintenanceRequest])
async def get_all_reports(db: Session = Depends(get_db)):
    return db.query(MaintenanceRequest).all()


