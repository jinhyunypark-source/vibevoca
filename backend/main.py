from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="VibeVoca AI Backend")

class HealthCheck(BaseModel):
    status: str
    version: str

@app.get("/", response_model=HealthCheck)
async def root():
    return {
        "status": "active", 
        "version": "0.1.0"
    }

@app.get("/health")
async def health():
    return {"status": "ok"}
