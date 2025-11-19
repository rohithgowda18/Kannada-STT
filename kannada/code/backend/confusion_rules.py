"""Confusion rules for the Modalapada Kannada Voice-to-Text Correction challenge.

This file contains:
- `CONFUSION_PAIRS`: pairs of visually or acoustically confusable Kannada letters (from the
  problem statement), used to suggest alternatives to the user.
- `OTTAKSHARA_PATTERNS`: common joined-letter (ottakshara) sequences and their logical
  split forms (for user verification).

The lists are intentionally conservative and mirror the examples in the problem statement.
Add more pairs as needed.
"""

# Confusable single-letter pairs (from the problem statement examples)
CONFUSION_PAIRS = [
    ("ವ", "ಮ"),  # ವ or ಮ
    ("ಪ", "ಫ"),  # ಪ or ಫ
    ("ಬ", "ಭ"),  # ಬ or ಭ
    ("ಠ", "ರ"),  # ಠ or ರ
]

# Example: other commonly-confused letters can be added here later if desired.

# Ottakshara (joined-letter) patterns mentioned in the statement with a suggested
# logical split (used to prompt the user whether the joined form is correct).
OTTAKSHARA_PATTERNS = [
    ("ಕ್ಕ", "ಕ್+ಕ್"),
    ("ತ್ತ", "ತ್+ತ್"),
    ("ನ್ನ", "ನ್+ನ್"),
]


def get_alternatives_for(char: str) -> list:
    """Return a list of alternative characters for a given character.

    If the character appears in any CONFUSION_PAIRS entry, return the pair (both options).
    Otherwise, return an empty list.
    """
    alts = []
    for a, b in CONFUSION_PAIRS:
        if char == a:
            alts = [a, b]
            break
        if char == b:
            alts = [b, a]
            break
    return alts


def find_ottakshara_matches(text: str) -> list:
    """Find ottakshara patterns in `text` and return list of matches.

    Each match is a tuple (pattern, logical_split, start_index).
    """
    matches = []
    for patt, logical in OTTAKSHARA_PATTERNS:
        start = 0
        while True:
            pos = text.find(patt, start)
            if pos == -1:
                break
            matches.append((patt, logical, pos))
            start = pos + 1
    return matches

