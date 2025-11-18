from typing import List, Dict

# Ottakshara pattern examples (very simplified)
PATTERNS = [
    ("ಕ್ ಕ್", "ಕ್ಕ"),
    ("ತ್ ತ", "ತ್ತ"),
    ("ನ್ ನ", "ನ್ನ"),
]


def detect_ottakshara(transcript: str) -> List[Dict]:
    """Detect simple ottakshara patterns and suggest combined forms."""
    results = []
    for frm, to in PATTERNS:
        if frm.replace(' ', '') in transcript.replace(' ', ''):
            results.append({"type": "ottakshara", "from": frm, "to": to})
    return results
