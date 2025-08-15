import os
from typing import Dict, Any
from fastapi import FastAPI, Body

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:29092")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

app = FastAPI(title="traffic_processor")

@app.get("/health")
def health() -> Dict[str, Any]:
    return {"ok": True, "kafka": KAFKA_BOOTSTRAP, "redis": REDIS_URL}

@app.post("/ingest")
def ingest(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    # In a future step, publish to Kafka and cache in Redis.
    # For now, just echo and pretend it's queued.
    return {"queued": True, "count": 1, "sample": payload}
