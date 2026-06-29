"""
maintenance_routes.py
----------------------
This module defines API endpoints for:
- Fetching all maintenance requests
- Fetching a single request by ID
- Updating technician reports for a request
- Fetching user accounts

It is structured as a FastAPI APIRouter so it can be cleanly imported
into the main FastAPI application using app.include_router().
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
import mysql.connector
import os

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
# Simple User Model (Not Pydantic)
# ------------------------------------------------------------
# Used only for returning database results in a structured format.
class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


# ------------------------------------------------------------
# GET /users
# ------------------------------------------------------------
# Returns all users stored in the database.
# Typically used by login or admin dashboard.
@router.get("/users")
def get_users():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT username, password FROM users")
        rows = cursor.fetchall()

        # Convert raw DB rows into User objects
        users = [User(username=row[0], password=row[1]) for row in rows]
        return users

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# ------------------------------------------------------------
# Ensure Upload Directory Exists
# ------------------------------------------------------------
# This directory stores uploaded images for maintenance requests.
os.makedirs("uploads", exist_ok=True)


# ------------------------------------------------------------
# GET /requests
# ------------------------------------------------------------
# Returns all maintenance requests in the database.
# Used by admin dashboard or technician interface.
@router.get("/requests")
def get_all_requests():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name, location, description, urgency, images
            FROM maintenance_requests
        """)

        # Convert DB rows into dictionaries for JSON response
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


# ------------------------------------------------------------
# GET /request/{id}
# ------------------------------------------------------------
# Returns a single maintenance request by its ID.
# Used when viewing or editing a specific request.
@router.get("/request/{id}")
def get_single_request(id: int):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name, location, description, urgency, images
            FROM maintenance_requests
            WHERE id = %s
        """, (id,))

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


# ------------------------------------------------------------
# PUT /request/{id}
# ------------------------------------------------------------
# Updates technician report fields for a specific request.
# This is used by maintenance staff to update:
# - Description
# - Images
# - Parts used
# - Warranty status
# - Technician report text
@router.put("/request/{id}")
def save_tech_report(
    id: int,
    description: str = Form(...),
    images: List[str] = Form(...),
    parts: List[str] = Form(...),
    warranty: str = Form(...)
):
    """
    Updates the technician report for a maintenance request.
    All fields are expected to be provided via multipart/form-data.
    """

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Update the request with technician data
        cursor.execute("""
            UPDATE maintenance_requests
            SET tech_report = %s,
                description = %s,
                images = %s,
                parts = %s,
                warranty = %s
            WHERE id = %s
        """,
        (
            description,
            ",".join(images),
            ",".join(parts),
            warranty,
            id
        ))

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
