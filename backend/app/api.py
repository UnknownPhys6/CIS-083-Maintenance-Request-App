#to run this application, go to the backend/app folder and run "python -m uvicorn api:app --reload"
from fastapi import FastAPI, HTTPException
from routes.maintenance_routes import router as maintenance_router

app = FastAPI()
app.include_router(maintenance_router)

@app.get("/")
def root():
    return {"message": "API is running"}