
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import uuid
import traceback
import json

from google.cloud import speech

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ai-gps-capstone-7df6af3a4c81.json"

@app.get("/map", response_class=HTMLResponse)
async def get_map():
    try:
        map_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "map.html"))
        with open(map_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return HTMLResponse(content=f"<h1>Map Load Error: {str(e)}</h1>", status_code=500)

from trip_logger import log_trip, suggest_better_route

@app.post("/analyze_route")
async def analyze_route(request: Request):
    try:
        data = await request.json()
        start = data.get("start")
        end = data.get("end")
        log_trip(start, end)
        tip = suggest_better_route(start, end)
        feedback = f"Simulated feedback for {start} → {end}"
        if tip:
            feedback += f"\n{tip}"
        return JSONResponse(content={"feedback": feedback})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    temp_filename = f"temp_{uuid.uuid4().hex}.webm"
    try:
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        client = speech.SpeechClient()

        with open(temp_filename, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            language_code="en-US"
        )

        response = client.recognize(config=config, audio=audio)

        if response.results:
            transcript = response.results[0].alternatives[0].transcript
            return {"text": transcript}
        else:
            return {"error": "No transcription results."}
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


@app.get("/address_suggestions")
async def address_suggestions(q: str = ""):
    try:
        suggestions = []
        data_path = os.path.join(os.path.dirname(__file__), "address_suggestions.json")
        if os.path.exists(data_path):
            with open(data_path, "r") as f:
                data = json.load(f)
                for addr in data.get("addresses", []):
                    if q.lower() in addr.lower():
                        suggestions.append(addr)
        return {"suggestions": suggestions[:5]}
    except Exception as e:
        return {"error": str(e)}
