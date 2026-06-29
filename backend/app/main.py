"""
main.py
--------
This is the central FastAPI application file.

Its responsibilities:
- Initialize the FastAPI app
- Configure global middleware (CORS)
- Register all route modules (routers)
- Provide a simple health-check endpoint

This file acts as the "entry point" for the backend.
All feature-specific routes live in separate modules and are included here.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers from other modules
# Each router contains its own endpoints and logic.
from .submit_request import router as submit_router
from .login import router as auth_router

# ------------------------------------------------------------
# FastAPI Application Initialization
# ------------------------------------------------------------
# This creates the main FastAPI app instance.
# All middleware, routers, and configuration attach to this object.
app = FastAPI()

# ------------------------------------------------------------
# CORS Configuration
# ------------------------------------------------------------
# CORS (Cross-Origin Resource Sharing) allows the frontend (React)
# to communicate with this backend even if they run on different ports.
#
# allow_origins=["*"] means ANY frontend can access the API.
# In production, you would restrict this to specific domains.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow all origins (React dev server, etc.)
    allow_credentials=True,
    allow_methods=["*"],          # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"]           # Allow all headers (tokens, content-type, etc.)
)

# ------------------------------------------------------------
# Router Registration
# ------------------------------------------------------------
# Routers allow the backend to be modular.
# Each feature (login, submit request, admin tools, etc.)
# lives in its own file and is included here.
#
# This keeps the backend clean, organized, and scalable.
app.include_router(submit_router)   # Public routes (submit request, fetch users)
app.include_router(auth_router)     # Authentication routes (login, token check)

# ------------------------------------------------------------
# Health Check Endpoint
# ------------------------------------------------------------
# Simple endpoint to verify the backend is running.
# Useful for debugging, monitoring, and frontend connectivity tests.
@app.get("/")
def home():
    return {"message": "Backend running"}
