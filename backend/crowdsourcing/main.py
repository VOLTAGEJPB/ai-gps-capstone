import os
from typing import Dict, Any, List
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "aimap")

app = FastAPI(title="crowdsourcing")

# Minimal in-memory fallback store if Mongo isn't available
MEM_STORE: List[Dict[str, Any]] = []

@app.get("/health")
def health() -> Dict[str, Any]:
    return {"ok": True, "mongo_url": MONGO_URL, "db": DB_NAME}

@app.post("/report")
def report(item: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    # In a future step, write to MongoDB.
    # For now, store in memory as a safe fallback.
    MEM_STORE.append(item)
    return {"stored": True, "total": len(MEM_STORE)}

@app.get("/reports")
def reports() -> JSONResponse:
    return JSONResponse(MEM_STORE)
