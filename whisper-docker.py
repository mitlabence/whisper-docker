from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import whisper
import os
from pathlib import Path
import shutil

MODEL_NAME = os.getenv("MODEL_NAME", "small")  # "small" as fallback model

app = FastAPI()

# Load the Whisper model once at startup
model = whisper.load_model(MODEL_NAME)

@app.post("/test")
def test_endpoint():
    return JSONResponse(content={"message": f"whisper-docker: running model {MODEL_NAME}"})

@app.get("/healthcheck")
def health_check():
    return JSONResponse(content={"status": "ok"})

@app.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    if audio.content_type not in ["audio/wav", "audio/mpeg", "audio/mp3", "audio/webm"]:
        raise HTTPException(status_code=400, detail="Unsupported audio type")

    # Save uploaded file temporarily
    tmp_dir = Path("/tmp")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_path = tmp_dir / audio.filename

    with tmp_path.open("wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    try:
        result = model.transcribe(str(tmp_path))
        return {"text": result["text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}") from e
    finally:
        tmp_path.unlink(missing_ok=True)
