FROM python:3.11-slim

# Install system dependencies for pyttsx3
RUN apt-get update && apt-get install -y \
    espeak \
    espeak-data \
    libespeak-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8002
CMD ["uvicorn", "tts:app", "--host", "0.0.0.0", "--port", "8002"]
