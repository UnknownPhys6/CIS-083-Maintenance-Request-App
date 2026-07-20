from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import db

router = APIRouter()

class RequestSearchFilters(BaseModel):
    active: bool | None = None
    urgency: int | None = None
    type: str | None = None
    assigned_to: str | None = None
    location: str | None = None
    sort_by: str = "id"
    order: str = "asc"
    limit: int = 50
    offset: int = 0

class MaintenanceResponse(BaseModel):
    id: int
    type: str
    urgency: int
    description: str
    location: str
    images: str | None = None
    assigned_to: str | None = None
    tech_comments: str | None = None
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
    assigned_to: str | None = None
    tech_comments: str | None = None
    urgency: str | None = None

"""
Returns maintenance requests with optional filtering, sorting, paging.
Here are some examples:
GET /requests?active=true
GET /requests?active=true&request_type=Electrical
GET /requests?sort_by=urgency&order=desc
GET /requests?limit=20&offset=40
"""
@router.get("/get_requests")
def get_requests(
    id: int | None = Query(None),
    active: bool | None = Query(None),
    urgency: int | None = Query(None),
    type: str | None = Query(None),
    assigned_to: str | None = Query(None),
    location: str | None = Query(None),
    sort_by: str = Query("id"),
    order: str = Query("asc"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    sql, values = build_request_query(
        id,
        active,
        urgency,
        type,
        assigned_to,
        location,
        sort_by,
        order,
        limit,
        offset
    )
    cnx = db.get_connection()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(sql, tuple(values))
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()
    return rows
def build_request_query(
    id,
    active,
    urgency,
    type,
    assigned_to,
    location,
    sort_by,
    order,
    limit,
    offset
):
    sql = "SELECT * FROM requests"
    conditions = []
    values = []

    # Filters
    if id is not None:
        conditions.append("id = %s")
        values.append(id)
    if active is not None:
        conditions.append("active = %s")
        values.append(active)
    if urgency is not None:
        conditions.append("urgency = %s")
        values.append(urgency)
    if type:
        conditions.append("type = %s")
        values.append(type)
    if assigned_to:
        conditions.append("assigned_to = %s")
        values.append(assigned_to)
    if location:
        conditions.append("location = %s")
        values.append(location)
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    # Sorting
    allowed_sort_columns = {
        "id",
        "type",
        "urgency",
        "description",
        "location",
        "assigned_To",
        "active"
    }
    if sort_by not in allowed_sort_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot sort by '{sort_by}'."
        )
    order = order.lower()
    if order not in ("asc", "desc"):
        raise HTTPException(
            status_code=400,
            detail="Order must be 'asc' or 'desc'."
        )
    sql += f" ORDER BY {sort_by} {order.upper()}"

    if id is not None:
        limit = 1

    # Pagination
    sql += " LIMIT %s OFFSET %s"
    values.append(limit)
    values.append(offset)
    return sql, values


@router.post("/create_maintenance_request")
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
        request_id = cursor.lastrowid
        cursor.close()
        cnx.close()
        return {
            "success": True,
            "message": "Request created successfully",
            "request_id": request_id
        }
    except Exception as e:
        print(e)
        raise

@router.put("/alter_request/{request_id}")
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

    if req.assigned_to is not None:
        fields.append("assigned_to = %s")
        values.append(req.assigned_to)

    if req.tech_comments is not None:
        fields.append("tech_comments = %s")
        values.append(req.tech_comments)

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
