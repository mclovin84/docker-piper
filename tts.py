from fastapi import FastAPI
from piper_tts import TTS

app = FastAPI()
tts = TTS()

@app.post("/synthesize")
async def synthesize(text: str):
    audio = tts.synthesize(text)
    return {"audio": audio}
