

from fastapi import APIRouter, HTTPException, Form, Header, Depends
import secrets

# ------------------------------------------------------------
# Router Initialization
# ------------------------------------------------------------
# APIRouter allows this file to define endpoints that can be
# included into the main FastAPI app using app.include_router().
router = APIRouter()

# ------------------------------------------------------------
# Hardcoded Credentials (Prototype Only)
# ------------------------------------------------------------
# These values represent the only valid login credentials.
# In a real system, credentials would be stored in a database
# and hashed using bcrypt or Argon2.
VALID_USERNAME = "admin"
VALID_PASSWORD = "7upisGood"

# ------------------------------------------------------------
# In‑Memory Session Store
# ------------------------------------------------------------
# This dictionary maps session tokens → username.
# It is wiped every time the server restarts.
#
# Example:
# sessions["a3f9c1..."] = "admin"
#
# In production, this would be replaced with:
# - JWT tokens
# - Redis session storage
# - Database‑backed sessions
sessions = {}


# ------------------------------------------------------------
# POST /auth/login
# ------------------------------------------------------------
# Validates username + password submitted via form data.
# If valid, generates a secure random token and stores it.
#
# The frontend should store this token (localStorage) and
# send it in the "token" header for protected routes.
@router.post("/auth/login")
def login(username: str = Form(...), password: str = Form(...)):
    # Check credentials against hardcoded values
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        # Generate a secure random session token
        token = secrets.token_hex(16)

        # Store the session
        sessions[token] = username

        # Return token to frontend
        return {"token": token}

    # Invalid credentials → 401 Unauthorized
    raise HTTPException(status_code=401, detail="Invalid username or password")


# ------------------------------------------------------------
# Authentication Dependency
# ------------------------------------------------------------
# This function is used with FastAPI's Depends() to protect routes.
#
# Any route that includes:
#     user = Depends(require_auth)
# will require a valid "token" header.
#
# If the token is missing or invalid, the request is rejected.
def require_auth(token: str = Header(None)):
    # Token must exist AND be stored in the session dictionary
    if token not in sessions:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Return the username associated with the token
    return sessions[token]


# ------------------------------------------------------------
# GET /auth/check
# ------------------------------------------------------------
# Protected endpoint that verifies whether the provided token
# is valid. Useful for:
# - Auto‑login checks
# - Protected page access
# - Session validation
@router.get("/auth/check")
def check_auth(user=Depends(require_auth)):
    return {
        "authorized": True,
        "user": user
    }

