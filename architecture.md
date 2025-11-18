# Architecture Overview

This document describes the high-level architecture for `kannada-voice-correction`.

- Frontend: Vite + React + Tailwind UI
- Backend: FastAPI exposing endpoints for transcription and detection
- Shared: sample paragraphs and audio for testing

Flow:
1. User uploads audio in the frontend.
2. Frontend sends audio to `/transcribe`.
3. Backend (Whisper) returns transcript and segments.
4. Backend runs detectors (confusable, ottakshara, dialect) and returns suggestions.
5. Frontend shows chips and suggestion cards; user applies corrections.
6. Frontend posts corrections to `/apply` and shows final polished text.
