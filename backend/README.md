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

Notes about Whisper and torch
--
The `whisper` package requires `torch`. Install the correct CPU wheel for your Python version using the PyTorch index. Example (CPU):

```powershell
# Use the PyTorch selector at https://pytorch.org/get-started/locally/ to get the right command.
# Example for Windows x86_64, Python 3.12, CPU-only:
python -m pip install --default-timeout=200 --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install whisper
```

If `transcribe` returns a warning about missing Whisper or torch, install `torch` and `whisper` into the active venv and restart the server.
