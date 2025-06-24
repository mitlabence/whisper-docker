FROM python:3.11-slim
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --upgrade pip

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Preload Whisper tiny model
RUN python3 -c "import whisper; whisper.load_model('tiny')"
COPY app.py .
# TODO: persist model cache: ENV XDG_CACHE_HOME=/app/cache then mount a volume to /app/cache
# expose the port that app.py uses
EXPOSE 5000  
CMD ["python", "app.py"]
