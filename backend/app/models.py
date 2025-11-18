from pydantic import BaseModel
from typing import List, Optional


class Segment(BaseModel):
    id: int
    start: float
    end: float
    text: str
    confidence: Optional[float]


class TranscribeResult(BaseModel):
    text: str
    segments: List[Segment]
