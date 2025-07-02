FROM python:3.11-slim

ARG MODEL_NAME=small
ENV MODEL_NAME=${MODEL_NAME}

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --upgrade pip

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Preload Whisper model
COPY setup.py .
RUN python setup.py

COPY whisper-docker.py .
# TODO: persist model cache: ENV XDG_CACHE_HOME=/app/cache then mount a volume to /app/cache
# expose the port that app.py uses
EXPOSE 5000  
CMD ["uvicorn", "whisper-docker:app", "--host", "0.0.0.0", "--port", "5000"]
