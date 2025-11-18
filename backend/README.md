# backend

This folder contains a FastAPI backend for the Kannada Voice Correction project.

Skeleton endpoints:
- `/transcribe` : accepts audio upload and returns Whisper-like JSON.
- `/detect` : detect confusables, ottakshara, and dialect suggestions from a transcript.
- `/apply` : apply corrections to a transcript.

To run locally (after creating a venv and installing `requirements.txt`):

```powershell
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Replace the placeholder stt implementation with actual Whisper model code when ready.
