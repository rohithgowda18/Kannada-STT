from typing import List, Dict

# Very small dialect mapping examples
DIALECT_MAP = {
    "ಹೋಗ್ತೀನಿ": "ಹೋಗುತ್ತೇನೆ",
    "ಮಾಡ್ತೀನಿ": "ಮಾಡುತ್ತೇನೆ",
}


def normalize_dialect(transcript: str) -> List[Dict]:
    results = []
    words = transcript.split()
    for i, w in enumerate(words):
        if w in DIALECT_MAP:
            results.append({"position": i, "from": w, "to": DIALECT_MAP[w]})
    return results
