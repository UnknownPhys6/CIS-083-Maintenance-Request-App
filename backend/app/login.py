from passlib.context import CryptContext
from fastapi import APIRouter, HTTPException, Form, Header, Depends
import secrets
from datetime import datetime, timedelta

from sqlalchemy.orm import Session as DBSession

from models import User, Session
from db import get_db

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
# -----------------------------------
# 
# -------------------------
# Router Initialization
# ------------------------------------------------------------
# APIRouter allows this file to define endpoints that can be
# included into the main FastAPI app using app.include_router().
router = APIRouter()


# ------------------------------------------------------------
# POST /auth/login
# ------------------------------------------------------------
# Validates username + password submitted via form data.
# If valid, generates a secure random token and stores it.
@router.post("/auth/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: DBSession = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not pwd_context.verify(password, user.hashedpass):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = secrets.token_hex(16)

    new_session = Session(
        user_id=user.id,
        token=token,
        expires=datetime.now() + timedelta(hours=24)
    )

    db.add(new_session)
    db.commit()

    return {"token": token}


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
def require_auth(
    token: str = Header(None),
    db: DBSession = Depends(get_db)
):
    session = db.query(Session).filter(
        Session.token == token
    ).first()

    if session is None:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    if session.expires < datetime.now():
        raise HTTPException(
            status_code=401,
            detail="Session expired"
        )

    return session.user_id


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

@router.post("/auth/logout")
def logout(
    token: str = Header(None),
    db: DBSession = Depends(get_db)
):
    db.query(Session).filter(
        Session.token == token
    ).delete()

    db.commit()

    return {"message": "Logged out"}