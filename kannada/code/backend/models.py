from pydantic import BaseModel
from typing import List, Literal, Optional

Level = Literal["easy", "medium", "hard"]

class ConfusionOption(BaseModel):
    id: str
    start_index: int
    end_index: int
    word: str
    detected_letter: str
    alternatives: List[str]
    user_picked: Optional[str] = None
    was_correct: Optional[bool] = None

class TranscriptionSession(BaseModel):
    session_id: str
    level: Level
    raw_text: str
    corrected_text: str
    confusions: List[ConfusionOption] = []

class DetectRequest(BaseModel):
    session_id: str
    level: Level
    text: str

class ApplyCorrectionsRequest(BaseModel):
    session_id: str
    corrections: List[ConfusionOption]
