from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount frontend directory to serve static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/map")
def serve_map():
    return FileResponse("frontend/map.html")

@app.get("/destination/{location}")
def get_route(location: str):
    return {"location": location, "route": f"Head north on Main Street to reach {location}."}

@app.get("/smart-detour/{location}")
def get_smart_detour(location: str):
    return {
        "location": location,
        "detour": f"Smart AI recommends avoiding central roads near {location}. Use Elm Street instead for faster access.",
        "reasoning": "High traffic detected due to nearby event activity."
    }
