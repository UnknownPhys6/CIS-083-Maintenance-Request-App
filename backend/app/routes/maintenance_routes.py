from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import db

router = APIRouter()

class MaintenanceResponse(BaseModel):
    id: int
    type: str
    urgency: str
    description: str
    location: str
    images: str | None = None
    assignedTo: str | None = None
    techComments: str | None = None
    active: bool

class CreateMaintenanceRequest(BaseModel):
    urgency: str
    type: str
    description: str
    location: str
    images: str | None = None
    active: bool

class UpdateRequest(BaseModel):
    description: str | None = None
    active: bool | None = None
    assignedTo: str | None = None
    techComments: str | None = None
    urgency: str | None = None


@router.get("/get_maintenance_requests", response_model=list[MaintenanceResponse])
def read_requests():
    try:
        cnx = db.get_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM requests")
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()
        return rows
    except Exception as e:
        print(e)
        raise

@router.post("/create_maintenance_requests")
def create_request(req: CreateMaintenanceRequest):
    try:  
        cnx = db.get_connection()
        cursor = cnx.cursor()
        cursor.execute(
            """
            INSERT INTO requests (type, urgency, description, location, images, active)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (req.type, req.urgency, req.description, req.location, req.images, req.active),
        )
        cnx.commit()
        cursor.close()
        cnx.close()
        return {"success": True, "message": "Request created successfully"}
    except Exception as e:
        print(e)
        raise

@router.put("/alter_maintenance_requests/{request_id}")
def update_request(request_id: int, req: UpdateRequest):
    cnx = db.get_connection()
    cursor = cnx.cursor()
    fields = []
    values = []
    # Check and append any fields provided in the request body
    if req.description is not None:
        fields.append("description = %s")
        values.append(req.description)

    if req.active is not None:
        fields.append("active = %s")
        values.append(req.active)

    if req.assignedTo is not None:
        fields.append("assignedTo = %s")
        values.append(req.assignedTo)

    if req.techComments is not None:
        fields.append("techComments = %s")
        values.append(req.techComments)

    if req.urgency is not None:
        fields.append("urgency = %s")
        values.append(req.urgency)

    # Prevent execution if the body was completely empty
    if not fields:
        cursor.close()
        cnx.close()
        raise HTTPException(status_code=400, detail="No fields provided for update")

    values.append(request_id)
    sql = f"""
        UPDATE requests
        SET {", ".join(fields)}
        WHERE id = %s
    """
    cursor.execute(sql, tuple(values))
    cnx.commit()
    cursor.close()
    cnx.close()
    return {"success": True}