from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .submit_request import router as submit_router
from .login import router as auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Public routes
app.include_router(submit_router)

# Auth + protected routes
app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "Backend running"}
