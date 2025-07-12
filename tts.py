from fastapi import FastAPI, HTTPException
import pyttsx3
import io
import base64
import tempfile
import os

app = FastAPI()

# Initialize TTS engine once at startup
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume level

@app.post("/synthesize")
async def synthesize(text: str):
    try:
        # Create a temporary file for the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_filename = temp_file.name
        
        # Generate speech and save to temp file
        engine.save_to_file(text, temp_filename)
        engine.runAndWait()
        
        # Read the generated audio file
        with open(temp_filename, 'rb') as audio_file:
            audio_data = audio_file.read()
        
        # Clean up temp file
        os.unlink(temp_filename)
        
        # Convert to base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        return {"audio": audio_base64, "format": "wav"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS synthesis failed: {str(e)}")
