from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from typing import List
import os

app = FastAPI()
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'maintenance_db'
}
class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
@app.get("/users")
def get_users():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM users")
        users = [User(username=row[0], password=row[1]) for row in cursor.fetchall()]
        return users
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Make sure upload folder exists
os.makedirs("uploads", exist_ok=True)
@app.get("/requests")
def get_all_requests():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT name, location, description, urgency, images FROM maintenance_requests")
        return [
    {
        "name": row[0],
        "location": row[1],
        "description": row[2],
        "urgency": row[3],
        "images": row[4]
    }
    for row in cursor.fetchall()
]

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
@app.get("/request/{id}")
def get_single_request(id: int):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT name, location, description, urgency, images FROM maintenance_requests WHERE id = %s", (id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Request not found")
        return {
        "name": row[0],
        "location": row[1],
        "description": row[2],
        "urgency": row[3],
        "images": row[4]
        }
    

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
@app.put("/request/{id}")
def save_tech_report(
    id: int,
    description: str = Form(...),
    images: List[str] = Form(...),
    parts: List[str] = Form(...),
    warranty: str = Form(...)
):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
    UPDATE maintenance_requests
    SET tech_report = %s,
        description = %s,
        images = %s,
        parts = %s,
        warranty = %s
    WHERE id = %s
    """, 
    (description,",".join(images),",".join(parts),warranty,id))

        conn.commit()
        return {"status": "success", "message": "Report saved"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
"""
TODO – Technician Side Remaining Work
-------------------------------------

- Add endpoint to update request status (open, in_progress, completed, etc.)
- Add endpoint to upload technician images (actual files, not just filenames)
- Add any missing database columns needed for tech fields
- Add error handling for invalid IDs or missing data
- Connect these endpoints to the technician UI in React
"""
