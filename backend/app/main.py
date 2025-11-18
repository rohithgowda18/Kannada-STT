from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from .stt import transcribe_audio
from .confusion_detector import detect_confusables
from .ottakshara import detect_ottakshara
from .dialect import normalize_dialect
from .utils import ensure_dir
import tempfile
import os
import csv
from datetime import datetime


app = FastAPI(title="Kannada Voice Correction - API")


@app.post('/transcribe')
async def transcribe(file: UploadFile = File(...)):
    """Transcribe uploaded audio using Whisper (backend uses `stt.transcribe_audio`).
    Saves the uploaded file to a temporary path and runs transcription.
    """
    contents = await file.read()
    tmp_dir = tempfile.gettempdir()
    tmp_path = os.path.join(tmp_dir, f"{datetime.utcnow().timestamp()}_{file.filename}")
    with open(tmp_path, 'wb') as f:
        f.write(contents)
    try:
        result = transcribe_audio(tmp_path)
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
    return JSONResponse(result)


@app.post('/detect')
async def detect(payload: dict):
    """Detect confusables, ottakshara, and dialect issues given a transcript."""
    transcript = payload.get('transcript', '')
    conf = detect_confusables(transcript)
    ott = detect_ottakshara(transcript)
    dial = normalize_dialect(transcript)
    return {"confusables": conf, "ottakshara": ott, "dialect_suggestions": dial}


@app.post('/apply')
async def apply_corrections(payload: dict):
    """Apply corrections to the transcript and return final text. Also append corrections to a CSV log.

    Expects: { transcript: str, corrections: [{position, replacement, original?, detected_letter?, alternatives?}] }
    """
    transcript = payload.get('transcript', '')
    corrections = payload.get('corrections', [])
    words = transcript.split()
    # Apply corrections
    for c in corrections:
        pos = c.get('position')
        repl = c.get('replacement')
        if pos is not None and 0 <= pos < len(words):
            words[pos] = repl
    final = ' '.join(words)

    # Log corrections to CSV
    logs_dir = os.path.join(os.getcwd(), 'backend', 'confusion_logs')
    ensure_dir(logs_dir)
    ts = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    csv_path = os.path.join(logs_dir, f'confusion_fixes_{ts}.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['position', 'word', 'detected_letter', 'alternatives', 'user_picked', 'was_correct'])
        for c in corrections:
            pos = c.get('position')
            original = c.get('original', '')
            detected = c.get('detected_letter', '')
            alternatives = '|'.join(c.get('alternatives', []))
            picked = c.get('replacement', '')
            was_correct = 'yes' if picked == detected else 'no'
            writer.writerow([pos, original, detected, alternatives, picked, was_correct])

    return {"final": final, "log_path": csv_path}



@app.get('/logs/{filename}')
async def get_log(filename: str):
    path = os.path.join(os.getcwd(), 'backend', 'confusion_logs', filename)
    if os.path.exists(path):
        return FileResponse(path, media_type='text/csv', filename=filename)
    return JSONResponse({'error': 'not found'}, status_code=404)
