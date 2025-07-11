
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/predict_route")
def predict_route(start_lat: float = Query(...), start_lng: float = Query(...), end_lat: float = Query(...), end_lng: float = Query(...)):
    return {
        "start": {"lat": start_lat, "lng": start_lng},
        "end": {"lat": end_lat, "lng": end_lng},
        "recommended_path": [
            {"lat": (start_lat + end_lat) / 2, "lng": (start_lng + end_lng) / 2},
            {"lat": end_lat, "lng": end_lng}
        ]
    }
