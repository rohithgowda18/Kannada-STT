from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from .stt import transcribe_audio
from .confusion_detector import detect_confusables
from .ottakshara import detect_ottakshara
from .dialect import normalize_dialect

app = FastAPI(title="Kannada Voice Correction - API")


@app.post('/transcribe')
async def transcribe(file: UploadFile = File(...)):
    """Return Whisper-like transcription result (placeholder).
    Expects audio file upload.
    """
    # Save uploaded file to disk (simple) and call transcribe_audio
    contents = await file.read()
    tmp_path = f"/tmp/{file.filename}"
    with open(tmp_path, 'wb') as f:
        f.write(contents)
    result = transcribe_audio(tmp_path)
    return JSONResponse(result)


@app.post('/detect')
async def detect(payload: dict):
    """Detect confusables, ottakshara, dialect issues given a transcript."""
    transcript = payload.get('transcript', '')
    conf = detect_confusables(transcript)
    ott = detect_ottakshara(transcript)
    dial = normalize_dialect(transcript)
    return {"confusables": conf, "ottakshara": ott, "dialect_suggestions": dial}


@app.post('/apply')
async def apply_corrections(payload: dict):
    """Apply corrections to the transcript and return final text."""
    transcript = payload.get('transcript', '')
    corrections = payload.get('corrections', [])
    # naive apply: iterate corrections list of {position, replacement}
    words = transcript.split()
    for c in corrections:
        pos = c.get('position')
        repl = c.get('replacement')
        if pos is not None and 0 <= pos < len(words):
            words[pos] = repl
    final = ' '.join(words)
    return {"final": final}
