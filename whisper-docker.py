from flask import Flask, request, jsonify
import whisper
import os

app = Flask(__name__)

# Load Whisper model (you can change to 'base', 'small', 'large', etc.)
model = whisper.load_model("turbo")

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    # TODO: might want to go lower level, see Python usage section in https://github.com/openai/whisper
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    audio_file = request.files["audio"]
    file_path = f"/tmp/{audio_file.filename}"
    audio_file.save(file_path)
    try:
        result = model.transcribe(file_path)
        return jsonify({"text": result["text"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(file_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
