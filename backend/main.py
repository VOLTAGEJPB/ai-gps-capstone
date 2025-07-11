from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI GPS App is live!"}

@app.get("/destination/{location}")
def get_directions(location: str):
    return {"directions": f"Route to {location} goes here (sample response)"}
