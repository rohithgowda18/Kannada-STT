from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, StreamingResponse
from typing import Dict
import io
import csv
import uuid
import os

from models import (
    TranscriptionSession,
    DetectRequest,
    ApplyCorrectionsRequest,
    ConfusionOption,
)
from confusion_rules import CONFUSION_PAIRS, OTTAKSHARA_PATTERNS

app = FastAPI(title="Kannada Voice-to-Text Correction")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory "database"
SESSIONS: Dict[str, TranscriptionSession] = {}

# ensure output directories exist
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RECORDINGS_DIR = os.path.join(ROOT, 'recordings')
TEXT_DIR = os.path.join(ROOT, 'text_outputs')
CSV_DIR = os.path.join(ROOT, 'confusion_fixes')
for d in (RECORDINGS_DIR, TEXT_DIR, CSV_DIR):
    os.makedirs(d, exist_ok=True)


# ------------------ STT (Speech-to-Text) ------------------ #

def dummy_stt() -> str:
    # TODO: replace with actual Google STT code
    # Return a short placeholder Kannada sentence for demo
    return "ನಮಸ್ಕಾರ, ಇದು ಒಂದು ಡೆಮೊ ಪಠ್ಯವಾಗಿದೆ."


@app.post("/api/transcribe")
async def transcribe_audio(
    level: str = Form(...),  # "easy" | "medium" | "hard"
    file: UploadFile = File(...)
):
    contents = await file.read()
    filename = f"{level}_paragraph_uploaded"
    save_path = os.path.join(RECORDINGS_DIR, f"{filename}")
    with open(save_path, "wb") as f:
        f.write(contents)

    # Replace this with actual STT call
    raw_text = dummy_stt()

    session_id = str(uuid.uuid4())
    session = TranscriptionSession(
        session_id=session_id,
        level=level,
        raw_text=raw_text,
        corrected_text=raw_text,
        confusions=[],
    )
    SESSIONS[session_id] = session

    # Also write original text file
    with open(os.path.join(TEXT_DIR, f"{level}_original.txt"), "w", encoding="utf-8") as f:
        f.write(raw_text)

    return {"session_id": session_id, "raw_text": raw_text}


# ------------------ Confusion Detection ------------------ #

@app.post("/api/detect-confusions")
async def detect_confusions(req: DetectRequest):
    if req.session_id not in SESSIONS:
        # create session if not exists (e.g. manual text)
        SESSIONS[req.session_id] = TranscriptionSession(
            session_id=req.session_id,
            level=req.level,
            raw_text=req.text,
            corrected_text=req.text,
            confusions=[],
        )

    session = SESSIONS[req.session_id]
    session.raw_text = req.text
    session.corrected_text = req.text

    text = req.text
    confusions: list[ConfusionOption] = []
    conf_id = 0

    # simple character-level scan
    for idx, ch in enumerate(text):
        for a, b in CONFUSION_PAIRS:
            if ch == a or ch == b:
                word = get_word_at(text, idx)
                confusions.append(
                    ConfusionOption(
                        id=f"c{conf_id}",
                        start_index=idx,
                        end_index=idx + 1,
                        word=word,
                        detected_letter=ch,
                        alternatives=[a, b],
                    )
                )
                conf_id += 1
                break

    # ottakshara patterns (simple substring match)
    for patt, logical in OTTAKSHARA_PATTERNS:
        start = 0
        while True:
            pos = text.find(patt, start)
            if pos == -1:
                break
            word = get_word_at(text, pos)
            confusions.append(
                ConfusionOption(
                    id=f"c{conf_id}",
                    start_index=pos,
                    end_index=pos + len(patt),
                    word=word,
                    detected_letter=patt,
                    alternatives=[patt, logical],
                )
            )
            conf_id += 1
            start = pos + 1

    session.confusions = confusions
    SESSIONS[req.session_id] = session

    return {"session_id": req.session_id, "confusions": [c.model_dump() for c in confusions]}


def get_word_at(text: str, index: int) -> str:
    # simple "split on space" word finder
    left = index
    right = index
    n = len(text)
    while left > 0 and text[left - 1] not in (" ", "\n"):
        left -= 1
    while right < n and text[right] not in (" ", "\n"):
        right += 1
    return text[left:right]


# ------------------ Apply Corrections ------------------ #

@app.post("/api/apply-corrections")
async def apply_corrections(req: ApplyCorrectionsRequest):
    if req.session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")

    session = SESSIONS[req.session_id]
    text_chars = list(session.raw_text)

    for c in req.corrections:
        # apply letter replacement
        if c.user_picked is not None:
            for i in range(c.start_index, c.end_index):
                text_chars[i] = ""  # clear first
            text_chars[c.start_index] = c.user_picked

    corrected = "".join(text_chars)
    session.corrected_text = corrected
    session.confusions = req.corrections
    SESSIONS[req.session_id] = session

    # Write corrected file
    level = session.level
    with open(os.path.join(TEXT_DIR, f"{level}_corrected.txt"), "w", encoding="utf-8") as f:
        f.write(corrected)

    # Write CSV log
    csv_path = os.path.join(CSV_DIR, f"{level}_fixes.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["position", "word", "detected_letter",
                         "alternatives", "user_picked", "was_correct"])
        for c in req.corrections:
            writer.writerow([
                c.start_index,
                c.word,
                c.detected_letter,
                "|".join(c.alternatives),
                c.user_picked or "",
                "yes" if c.was_correct else "no" if c.was_correct is not None else "",
            ])

    return {"session_id": req.session_id, "corrected_text": corrected}


# ------------------ Export Endpoints ------------------ #

@app.get("/api/export/text", response_class=PlainTextResponse)
async def export_text(session_id: str, kind: str = "corrected"):
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")
    session = SESSIONS[session_id]
    return session.corrected_text if kind == "corrected" else session.raw_text


@app.get("/api/export/confusions")
async def export_confusions(session_id: str):
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")
    session = SESSIONS[session_id]

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["position", "word", "detected_letter",
                     "alternatives", "user_picked", "was_correct"])
    for c in session.confusions:
        writer.writerow([
            c.start_index,
            c.word,
            c.detected_letter,
            "|".join(c.alternatives),
            c.user_picked or "",
            "yes" if c.was_correct else "no" if c.was_correct is not None else "",
        ])

    buffer.seek(0)
    return StreamingResponse(
        iter([buffer.getvalue().encode("utf-8")]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=confusions.csv"},
    )
