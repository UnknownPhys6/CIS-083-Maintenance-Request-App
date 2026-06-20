from fastapi import FastAPI
import db
from pydantic import BaseModel

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


class UpdateRequest(BaseModel):
    requestDesc: str | None = None
    active: int | None = None

@app.put("/maintenance_requests/{request_id}")
def update_request(request_id: int, req: UpdateRequest):
    cnx = db.get_connection()
    cursor = cnx.cursor()
    fields = []
    values = []
    if req.active is not None:
        fields.append("active = %s")
        values.append(req.active)

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

