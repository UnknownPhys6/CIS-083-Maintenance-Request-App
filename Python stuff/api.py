from fastapi import FastAPI, HTTPException
import db
from pydantic import BaseModel
import uvicorn

app = FastAPI()
@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/maintenance_requests")
def read_requests():
    cnx = db.get_connection()
    cursor = cnx.cursor(dictionary=True)

    cursor.execute("SELECT * FROM requests")
    rows = cursor.fetchall()

    cursor.close()
    cnx.close()
    return rows


class MaintenanceRequest(BaseModel):
    requestType: str
    requestDesc: str
    requestLocation: str
    active: bool


@app.post("/maintenance_requests")
def create_request(req: MaintenanceRequest):
    cnx = db.get_connection()
    cursor = cnx.cursor()
    cursor.execute(
        """
        INSERT INTO requests (requestType, requestDesc, requestLocation, active)
        VALUES (%s, %s, %s, %s)
        """,
        (req.requestType, req.requestDesc, req.requestLocation, req.active),
    )
    cnx.commit()
    cursor.close()
    cnx.close()
    return {"success": True, "message": "Request created successfully"}


class UpdateRequest(BaseModel):
    requestDesc: str | None = None
    active: bool | None = None  # Changed int to bool to match standard schema


@app.put("/maintenance_requests/{request_id}")
def update_request(request_id: int, req: UpdateRequest):
    cnx = db.get_connection()
    cursor = cnx.cursor()

    fields = []
    values = []

    # Safely handle both potential update fields
    if req.requestDesc is not None:
        fields.append("requestDesc = %s")
        values.append(req.requestDesc)

    if req.active is not None:
        fields.append("active = %s")
        values.append(req.active)

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

# Added the execution block with public host binding for port forwarding
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
