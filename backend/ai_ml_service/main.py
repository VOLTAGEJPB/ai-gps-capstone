from typing import Dict, Any
from fastapi import FastAPI, Body

app = FastAPI(title="ai_ml_service")

@app.get("/health")
def health() -> Dict[str, Any]:
    return {"ok": True, "model": "stub"}

@app.post("/route/analyze")
def analyze_route(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    # Stub logic. Replace with ONNX / TF later.
    start = payload.get("start")
    end = payload.get("end")
    return {
        "ok": True,
        "advice": [
            "Leave 5–10 minutes earlier to avoid peak congestion.",
            "Watch for police reports near major intersections.",
            "Alternative route B saves ~3 minutes with current traffic."
        ],
        "start": start,
        "end": end
    }
