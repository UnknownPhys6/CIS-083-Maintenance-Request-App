"""
submit_request.py
------------------
This module defines the API routes responsible for:
- Fetching user accounts
- Submitting new maintenance requests
- Uploading images associated with requests
- Preventing duplicate submissions using similarity detection

It is structured as a FastAPI APIRouter so it can be cleanly imported
into the main FastAPI application.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
import os
import mysql.connector

# ------------------------------------------------------------
# Router Initialization
# ------------------------------------------------------------
# APIRouter allows this file to define endpoints that can be
# included into the main FastAPI app using app.include_router().
router = APIRouter()

# ------------------------------------------------------------
# Database Configuration
# ------------------------------------------------------------
# These credentials define how the backend connects to MySQL.
# The database name must match the schema created in MySQL.
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Group2pass',
    'database': "maintenance_requests",
    'port': 3306
}

# ------------------------------------------------------------
# Upload Directory Setup
# ------------------------------------------------------------
# Ensures the "uploads" directory exists so uploaded images
# can be saved without causing a filesystem error.
os.makedirs("uploads", exist_ok=True)


# ------------------------------------------------------------
# User Model (Simple Python Class)
# ------------------------------------------------------------
# This is NOT a Pydantic model. It is used only for returning
# database results in a structured format.
class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


# ------------------------------------------------------------
# GET /users
# ------------------------------------------------------------
# Returns all users stored in the database.
# This is typically used by the login page or admin dashboard.
@router.get("/users")
def get_users():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch username + password for all users
        cursor.execute("SELECT username, password FROM users")
        rows = cursor.fetchall()

        # Convert raw DB rows into User objects
        users = [User(username=row[0], password=row[1]) for row in rows]
        return users

    except mysql.connector.Error as err:
        # Any database error results in a 500 response
        raise HTTPException(status_code=500, detail=str(err))

    finally:
        # Always close DB connections to prevent leaks
        if conn.is_connected():
            cursor.close()
            conn.close()


# ------------------------------------------------------------
# Duplicate Request Detection
# ------------------------------------------------------------
# Compares the submitted description with existing descriptions.
# If more than 3 words overlap, the request is considered a duplicate.
def is_similar(description: str, existing_descriptions: List[str]) -> bool:
    description_words = set(description.lower().split())

    for old in existing_descriptions:
        old_words = set(old.lower().split())
        overlap = description_words & old_words

        # If 3+ words match, assume the request is already submitted
        if len(overlap) > 3:
            return True

    return False


# ------------------------------------------------------------
# POST /submit
# ------------------------------------------------------------
# Handles full maintenance request submission including:
# - Form fields
# - Uploaded images
# - Duplicate detection
# - Database insertion
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
    """
    Receives a maintenance request from the frontend form.
    Saves uploaded images, checks for duplicates, and inserts
    the request into the MySQL database.
    """

    # ------------------------------------------------------------
    # Save Uploaded Images
    # ------------------------------------------------------------
    saved_files = []

    if images:
        for img in images:
            contents = await img.read()
            file_path = f"uploads/{img.filename}"

            # Write the uploaded file to disk
            with open(file_path, "wb") as f:
                f.write(contents)

            saved_files.append(img.filename)

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # ------------------------------------------------------------
        # Duplicate Request Check
        # ------------------------------------------------------------
        check_query = """
            SELECT description
            FROM maintenance_requests
            WHERE name = %s AND location = %s
        """
        cursor.execute(check_query, (name, location))
        existing_descriptions = [row[0] for row in cursor.fetchall()]

        if is_similar(description, existing_descriptions):
            raise HTTPException(
                status_code=400,
                detail="Request already exists"
            )

        # ------------------------------------------------------------
        # Insert New Request Into Database
        # ------------------------------------------------------------
        insert_query = """
            INSERT INTO maintenance_requests
            (name, location, area_type, category, description, urgency, images)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            insert_query,
            (
                name,
                location,
                area_type,
                category,
                description,
                urgency,
                ",".join(saved_files)
            )
        )

        conn.commit()

    except mysql.connector.Error as err:
        # Any SQL or connection error results in a 500 response
        raise HTTPException(status_code=500, detail=str(err))

    finally:
        # Always close DB resources
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()

    # ------------------------------------------------------------
    # Successful Response
    # ------------------------------------------------------------
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
"""
