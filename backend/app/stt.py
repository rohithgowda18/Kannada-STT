def transcribe_audio(path: str) -> dict:
    """Placeholder wrapper for Whisper transcription.
    Replace with actual whisper model load and transcription.
    """
    # Minimal fake response for scaffolding
    return {
        "text": "ಓದುದಿಲ್ಲ ಉದಾಹರಣೆ ಓದುವಿಕೆಯಿಗಾಗಿ",
        "segments": [
            {"id": 0, "start": 0.0, "end": 2.0, "text": "ಓದುದಿಲ್ಲ", "confidence": 0.85},
            {"id": 1, "start": 2.0, "end": 4.0, "text": "ಉದಾಹರಣೆ", "confidence": 0.72},
        ],
    }
