# whisper-docker
A Docker container running OpenAI's whisper as a service.

# How-to
Select the model (`tiny`, `small`, `turbo` etc, see available models on the whisper [github repo](https://github.com/openai/whisper)) by changing it in the Dockerfile and the app.py files.

Then build the docker container when in the repo directory:
`docker build -t whisper-server-tiny .`


Run it (listening on port 5000):
`docker run -p 5000:5000 whisper-server-tiny`



`curl -X POST -F "audio=@C:\example.mp3" http://localhost:5000/transcribe`
