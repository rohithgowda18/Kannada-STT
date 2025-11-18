"""Whisper STT wrapper.

This module tries to load the whisper model once and reuse it for subsequent calls.
If `whisper` or `torch` is not available, it falls back to a placeholder response.
"""
from typing import Dict
import os

MODEL_NAME = os.environ.get('WHISPER_MODEL', 'small')
_model = None

def _load_model():
    global _model
    if _model is not None:
        return _model
    try:
        import whisper
    except Exception:
        _model = None
        return None
    try:
        # load model (this may download weights on first run)
        _model = whisper.load_model(MODEL_NAME)
    except Exception:
        _model = None
    return _model


def transcribe_audio(path: str) -> Dict:
    """Transcribe the audio file at `path` using Whisper.

    Returns a dict with keys: text, segments (list of {id,start,end,text,confidence}).
    """
    model = _load_model()
    if model is None:
        # fallback placeholder if whisper is not available
        return {
            "text": "",
            "segments": [],
            "warning": "Whisper model not available on server. Install 'whisper' and 'torch' to enable transcription."
        }

    # use language='kn' to bias Kannada
    result = model.transcribe(path, language='kn')
    # Normalize segments
    segments = []
    for i, s in enumerate(result.get('segments', [])):
        segments.append({
            'id': i,
            'start': s.get('start'),
            'end': s.get('end'),
            'text': s.get('text').strip(),
            'confidence': s.get('no_speech_prob', None) if 'no_speech_prob' in s else None
        })
    return { 'text': result.get('text','').strip(), 'segments': segments }
