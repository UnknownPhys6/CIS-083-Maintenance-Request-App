from fastapi import FastAPI, HTTPException
import db
from pydantic import BaseModel
import uvicorn

app = FastAPI()
@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/get_maintenance_requests")
def read_requests():
    cnx = db.get_connection()
    cursor = cnx.cursor(dictionary=True)

    cursor.execute("SELECT * FROM requests")
    rows = cursor.fetchall()

    cursor.close()
    cnx.close()
    return rows


class MaintenanceRequest(BaseModel):
    requestUrgency: str
    requestType: str
    requestDesc: str
    requestLocation: str
    active: bool

@app.post("/create_maintenance_requests")
def create_request(req: MaintenanceRequest):
    cnx = db.get_connection()
    cursor = cnx.cursor()
    cursor.execute(
        """
        INSERT INTO requests (type, urgency, description, location, images, active)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (req.requestUrgency, req.requestType, req.requestDesc, req.requestLocation, req.supportingFiles, req.active),
    )
    cnx.commit()
    cursor.close()
    cnx.close()
    return {"success": True, "message": "Request created successfully"}


class UpdateRequest(BaseModel):
    description: str | None = None
    active: bool | None = None
    assignedTo: str | None = None
    techComments: str | None = None
    urgency: str | None = None  # Adjust type (e.g., int) if your DB uses numbers for urgency

@app.put("/alter_maintenance_requests/{request_id}")
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
        WHERE requestID = %s
    """

    cursor.execute(sql, tuple(values))
    cnx.commit()

    cursor.close()
    cnx.close()

    return {"success": True}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
