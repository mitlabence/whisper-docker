import os
import whisper
MODEL_NAME = os.getenv("MODEL_NAME", "small")  # "small" as fallback model
whisper.load_model(MODEL_NAME)
print(f"Whisper model {MODEL_NAME} loaded successfully.")