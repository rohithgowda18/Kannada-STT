from typing import List, Dict

# Simple confusable pairs for Kannada (expandable)
CONFUSABLES = [
    ("ವ", "ಮ"),
    ("ಪ", "ಫ"),
    ("ಬ", "ಭ"),
    ("ತ", "ಥ"),
    ("ಡ", "ಢ"),
]


def detect_confusables(transcript: str) -> List[Dict]:
    """Detect simple confusable characters/words in a transcript.
    Returns list of suggestions with word, position and alternatives.
    """
    words = transcript.split()
    results = []
    for i, w in enumerate(words):
        for a, b in CONFUSABLES:
            if a in w:
                results.append({"word": w, "position": i, "type": "confusable", "suggestions": [w.replace(a, b)]})
            elif b in w:
                results.append({"word": w, "position": i, "type": "confusable", "suggestions": [w.replace(b, a)]})
    return results
