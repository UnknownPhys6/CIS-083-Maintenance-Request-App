#to run this application, go to the backend/app folder and run "python -m uvicorn api:app --reload"
from fastapi import FastAPI, HTTPException
from routes.maintenance_routes import router as maintenance_router
from fastapi.middleware.cors import CORSMiddleware
from .submit_request import router as submit_router
from .login import router as auth_router
from .maintence_logic import router as maintenance_router
app = FastAPI()
app.include_router(maintenance_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow all origins (React dev server, etc.)
    allow_credentials=True,
    allow_methods=["*"],          # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"]           # Allow all headers (tokens, content-type, etc.)
)
@app.get("/")
def root():
    return {"message": "API is running"}