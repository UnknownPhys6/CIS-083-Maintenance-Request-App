from fastapi import APIRouter, HTTPException, Form, Header, Depends
import secrets

router = APIRouter()

VALID_USERNAME = "admin"
VALID_PASSWORD = "7upisGood"

sessions = {}  # simple in-memory session store

@router.post("/auth/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        token = secrets.token_hex(16)
        sessions[token] = username
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid username or password")


def require_auth(token: str = Header(None)):
    if token not in sessions:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return sessions[token]


@router.get("/auth/check")
def check_auth(user=Depends(require_auth)):
    return {"authorized": True, "user": user}
