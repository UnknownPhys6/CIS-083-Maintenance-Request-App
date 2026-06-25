from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
import os
import mysql.connector


router = APIRouter()
db_config = {
    'host': 'localhost', 
    'user': 'root',
    'password': 'Group2pass',
    'database': "maintenance_requests",
    'port': 3306
}
os.makedirs("uploads", exist_ok=True) 

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
@router.get("/users")
def get_users():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM users")
        rows = cursor.fetchall()
        users = [User(username=row[0], password=row[1]) for row in rows]
        return users
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def is_similar(description: str, existing_descriptions: List[str]) -> bool:
    description_words = set(description.lower().split())
    
    for old in existing_descriptions:
        old_words = set(old.lower().split())
        overlap = description_words & old_words
        if len(overlap) > 3:
            return True
    return False

@router.post("/submit")
async def submit_request(
    name: str = Form(...),
    location: str = Form(...),
    area_type: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    urgency: str = Form(...),
    images: List[UploadFile] | None = File(None),
):
    
    saved_files = []
    if images:
        for img in images:
            contents = await img.read()
            file_path = f"uploads/{img.filename}"
            with open(file_path, "wb") as f:
                f.write(contents)
            saved_files.append(img.filename)
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        #Check for similar existing requests
        check_query = "SELECT description FROM maintenance_requests WHERE name = %s AND location = %s"
        cursor.execute(check_query, (name, location))
        existing_descriptions = [row[0] for row in cursor.fetchall()]

        if is_similar(description, existing_descriptions):
            raise HTTPException(status_code=400, detail="Request already exists")

        cursor.execute(
            "INSERT INTO maintenance_requests (name, location, area_type, category, description, urgency, images) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (name, location, area_type, category, description, urgency, ",".join(saved_files))
        )
        conn.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()
    return {
        "status": "success",
        "message": "Request submitted successfully",
        "data": {
            "name": name,
            "location": location,
            "area_type": area_type,
            "category": category,
            "description": description,
            "urgency": urgency,
            "images": saved_files
        }
    
    }



"""
TODO – User Submission Side Remaining Work
------------------------------------------

- Add validation for missing fields (name, location, area_type, category,   description, urgency)
- Add better duplicate‑request detection if needed
- Add endpoint to fetch user‑submitted images if the UI needs them
- Add error handling for failed uploads or database issues
- Connect this backend to the user-facing React form
- Add urgency, area_type, and images, as well as one named tech_comments or something similar
"""
