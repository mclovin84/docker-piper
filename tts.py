from fastapi import FastAPI
from wyoming_piper import PiperTTS

app = FastAPI()
tts = PiperTTS()

@app.post("/synthesize")
async def synthesize(text: str):
    audio = tts.synthesize(text)
    return {"audio": audio}
