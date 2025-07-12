from fastapi import FastAPI, HTTPException
import subprocess
import tempfile
import os
import base64

app = FastAPI()

@app.post("/synthesize")
async def synthesize(text: str):
    try:
        # Create a temporary file for the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_filename = temp_file.name
        
        # Use espeak directly via subprocess
        cmd = [
            'espeak',
            '-w', temp_filename,  # Write to file
            '-s', '150',          # Speed (words per minute)
            '-v', 'en',           # Voice (English)
            text
        ]
        
        # Run espeak
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"espeak failed: {result.stderr}")
        
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
